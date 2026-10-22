import argparse
import importlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageSequence


CELL = (192, 208)
BACKGROUND = "#f1f7ef"
INK = "#1f4936"
TRANSPARENT = 255
ROW_DURATIONS = {
    "idle": [280, 110, 110, 140, 140, 320],
    "running-right": [120, 120, 120, 120, 120, 120, 120, 220],
    "running-left": [120, 120, 120, 120, 120, 120, 120, 220],
    "waving": [140, 140, 140, 280],
    "jumping": [140, 140, 140, 140, 280],
    "failed": [140, 140, 140, 140, 140, 140, 140, 240],
    "waiting": [150, 150, 150, 150, 150, 260],
    "running": [120, 120, 120, 120, 120, 220],
    "review": [150, 150, 150, 150, 150, 280],
}
LABELS = {
    "idle": "Blinking",
    "running-right": "Running right",
    "running-left": "Running left",
    "waving": "Hello!",
    "jumping": "Happy hop",
    "failed": "Oops...",
    "waiting": "Pretty please?",
    "running": "Thinking",
    "review": "Looking good",
}


def font(size):
    return ImageFont.load_default(size=size)


def make_palette(frames):
    samples = bytearray()
    for frame in frames:
        rgba = frame.convert("RGBA").tobytes()
        samples.extend(
            channel
            for index in range(0, len(rgba), 4)
            if rgba[index + 3] >= 128
            for channel in rgba[index : index + 3]
        )
    if not samples:
        raise ValueError("The supplied frames are fully transparent")
    count = len(samples) // 3
    stride = max(1, (count + 262143) // 262144)
    samples = b"".join(samples[index : index + 3] for index in range(0, len(samples), stride * 3))
    count = len(samples) // 3
    sample = Image.frombytes("RGB", (count, 1), samples)
    quantized = sample.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    colors = quantized.getpalette()[:765]
    colors += [0] * (765 - len(colors))
    colors += colors[:3]
    palette = Image.new("P", (1, 1))
    palette.putpalette(colors)
    return palette


def indexed_frame(frame, palette):
    rgba = frame.convert("RGBA")
    indexed = rgba.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
    pixels = bytearray(indexed.tobytes())
    alpha = rgba.getchannel("A").tobytes()
    for index, opacity in enumerate(alpha):
        if opacity < 128:
            pixels[index] = TRANSPARENT
        elif pixels[index] == TRANSPARENT:
            pixels[index] = 0
    result = Image.frombytes("P", frame.size, bytes(pixels))
    result.putpalette(palette.getpalette())
    result.info["transparency"] = TRANSPARENT
    return result


def save_gif(frames, durations, destination, palette=None):
    if len(frames) != len(durations):
        raise ValueError(f"Frame and duration counts differ for {destination}")
    palette = palette or make_palette(frames)
    indexed = [indexed_frame(frame, palette) for frame in frames]
    destination.parent.mkdir(parents=True, exist_ok=True)
    indexed[0].save(
        destination,
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
        transparency=TRANSPARENT,
        background=TRANSPARENT,
        palette=bytes(palette.getpalette()),
    )


def labeled(cell, label, scale=2):
    width, height = CELL[0] * scale, CELL[1] * scale
    result = Image.new("RGBA", (width, height + 32), BACKGROUND)
    result.alpha_composite(cell.resize((width, height), Image.Resampling.LANCZOS))
    draw = ImageDraw.Draw(result)
    label_font = font(20)
    bounds = draw.textbbox((0, 0), label, font=label_font)
    draw.text(((width - bounds[2]) / 2, height + 3), label, font=label_font, fill=INK)
    return result


def collect(cells, states, with_labels):
    frames, durations = [], []
    for state in states:
        frames.extend(labeled(cell, LABELS[state]) if with_labels else cell for cell in cells[state])
        durations.extend(ROW_DURATIONS[state])
    return frames, durations


def save_contact_sheet(cells, destination):
    row_height = 240
    result = Image.new("RGBA", (CELL[0] * 8, row_height * len(cells)), BACKGROUND)
    draw = ImageDraw.Draw(result)
    label_font = font(18)
    for row, (state, frames) in enumerate(cells.items()):
        draw.text((12, row * row_height + 5), state, font=label_font, fill=INK)
        for column, frame in enumerate(frames):
            result.alpha_composite(frame, (column * CELL[0], row * row_height + 30))
    result.convert("RGB").save(destination)


def save_look_sheet(frames, destination):
    width, height = CELL[0], CELL[1] + 32
    result = Image.new("RGBA", (width * 4, height * 4), BACKGROUND)
    for index, frame in enumerate(frames):
        result.alpha_composite(labeled(frame, f"Look {index + 1:02}", scale=1), ((index % 4) * width, (index // 4) * height))
    result.convert("RGB").save(destination)


def save_motion_stills(cells, destination):
    poses = [("idle", 0), ("waving", 1), ("jumping", 2), ("waiting", 2)]
    result = Image.new("RGBA", (768, 896), BACKGROUND)
    for index, (state, frame) in enumerate(poses):
        result.alpha_composite(labeled(cells[state][frame], LABELS[state]), ((index % 2) * 384, (index // 2) * 448))
    result.convert("RGB").save(destination)


def load_ffmpeg(tools_dir):
    if tools_dir is not None:
        sys.path.insert(0, str(tools_dir))
    return importlib.import_module("imageio_ffmpeg")


def save_video(frames, durations, destination, tools_dir):
    ffmpeg = load_ffmpeg(tools_dir)
    writer = ffmpeg.write_frames(
        str(destination),
        frames[0].size,
        fps=100,
        codec="libx264",
        pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p",
        macro_block_size=1,
        ffmpeg_log_level="error",
    )
    writer.send(None)
    try:
        for frame, duration in zip(frames, durations):
            encoded = frame.convert("RGB").tobytes()
            for _ in range(duration // 10):
                writer.send(encoded)
    finally:
        writer.close()


def inspect_gifs(output_dir):
    results = []
    for path in sorted(output_dir.rglob("*.gif")):
        with Image.open(path) as opened:
            results.append({
                "file": path.relative_to(output_dir).as_posix(),
                "size": list(opened.size),
                "frames": opened.n_frames,
                "duration_ms": sum(frame.info.get("duration", 0) for frame in ImageSequence.Iterator(opened)),
            })
    return results


def validate_gif(frames, durations, path):
    with Image.open(path) as opened:
        if opened.size != CELL or opened.n_frames != len(durations):
            raise ValueError(f"Wrong dimensions or frame count for {path.name}")
        if opened.info.get("transparency") != TRANSPARENT:
            raise ValueError(f"Missing reserved transparent index for {path.name}")
        mismatches = 0
        actual_durations = []
        for source, frame in zip(frames, ImageSequence.Iterator(opened)):
            expected = source.getchannel("A").point(lambda alpha: 255 if alpha >= 128 else 0).tobytes()
            actual = frame.convert("RGBA").getchannel("A").tobytes()
            mismatches += sum(left != right for left, right in zip(expected, actual))
            actual_durations.append(frame.info.get("duration", 0))
        if mismatches or actual_durations != durations:
            raise ValueError(f"Alpha mask or timings differ for {path.name}: {mismatches} pixels")
        return {"frames": len(durations), "alpha_mismatches": mismatches, "timings_exact": True}


def validate_exports(atlas, output_dir):
    cells = {
        state: [atlas.crop((column * CELL[0], row * CELL[1], (column + 1) * CELL[0], (row + 1) * CELL[1])) for column in range(len(durations))]
        for row, (state, durations) in enumerate(ROW_DURATIONS.items())
    }
    results = [
        {"state": state, **validate_gif(cells[state], durations, output_dir / "animations" / f"{state}.gif")}
        for state, durations in ROW_DURATIONS.items()
    ]
    sequences = []
    for name, states in [
        ("cute.gif", ["idle", "waving", "jumping", "waiting"]),
        ("animations/idle-jump-idle.gif", ["idle", "jumping", "idle"]),
    ]:
        frames, durations = collect(cells, states, False)
        sequences.append({"file": name, **validate_gif(frames, durations, output_dir / name)})
    return {"ok": True, "atlas": "spritesheet.png", "states": results, "sequences": sequences, "total_state_frames": sum(item["frames"] for item in results)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ffmpeg-tools", type=Path)
    parser.add_argument("--validate", action="store_true", help="Validate existing state GIFs without rendering or loading FFmpeg")
    args = parser.parse_args()
    with Image.open(args.atlas) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (CELL[0] * 8, CELL[1] * 11):
        raise ValueError(f"Expected a 1536x2288 extended atlas, found {atlas.size}")
    if args.validate:
        result = validate_exports(atlas, args.output_dir)
        (args.output_dir / "validation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        return
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cells = {
        state: [atlas.crop((column * CELL[0], row * CELL[1], (column + 1) * CELL[0], (row + 1) * CELL[1])) for column in range(len(durations))]
        for row, (state, durations) in enumerate(ROW_DURATIONS.items())
    }
    looks = [atlas.crop((column * CELL[0], row * CELL[1], (column + 1) * CELL[0], (row + 1) * CELL[1])) for row in (9, 10) for column in range(8)]
    palette = make_palette([frame for frames in cells.values() for frame in frames] + looks)
    for state, frames in cells.items():
        save_gif(frames, ROW_DURATIONS[state], args.output_dir / "animations" / f"{state}.gif", palette)
    cute_frames, cute_durations = collect(cells, ["idle", "waving", "jumping", "waiting"], False)
    save_gif(cute_frames, cute_durations, args.output_dir / "cute.gif", palette)
    transition_frames, transition_durations = collect(cells, ["idle", "jumping", "idle"], False)
    save_gif(transition_frames, transition_durations, args.output_dir / "animations" / "idle-jump-idle.gif", palette)
    preview_frames, preview_durations = collect(cells, cells, True)
    save_gif(preview_frames, preview_durations, args.output_dir / "preview.gif")
    look_frames = [labeled(frame, f"Look {index + 1:02}") for index, frame in enumerate(looks)]
    save_gif(look_frames, [150] * len(look_frames), args.output_dir / "look.gif")
    save_video(preview_frames, preview_durations, args.output_dir / "preview.mp4", args.ffmpeg_tools)
    save_contact_sheet(cells, args.output_dir / "contact-sheet.png")
    save_look_sheet(looks, args.output_dir / "look-directions.png")
    save_motion_stills(cells, args.output_dir / "motion-stills.png")
    result = {"ok": True, "atlas": args.atlas.name, "previews": inspect_gifs(args.output_dir)}
    (args.output_dir / "export-report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
