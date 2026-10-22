"""Fit six generated poses per quiet state and preserve every other atlas cell.

Artwork must already come from image generation. This tool only extracts,
registers, composes, losslessly encodes and measures existing pixels.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

CELL = (192, 208)
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
ROWS = {"idle": 0, "running": 7}


def components(image):
    visible = np.array(image.getchannel("A")) > 16
    height, width = visible.shape
    result = []
    for y in range(height):
        for x in np.flatnonzero(visible[y]):
            if not visible[y, x]:
                continue
            queue = deque([(int(x), y)])
            visible[y, x] = False
            left = right = int(x)
            top = bottom = y
            area = 0
            while queue:
                cx, cy = queue.pop()
                area += 1
                left, right = min(left, cx), max(right, cx)
                top, bottom = min(top, cy), max(bottom, cy)
                for ny in range(max(0, cy - 1), min(height, cy + 2)):
                    for nx in range(max(0, cx - 1), min(width, cx + 2)):
                        if visible[ny, nx]:
                            visible[ny, nx] = False
                            queue.append((nx, ny))
            result.append({"area": area, "bbox": [left, top, right + 1, bottom + 1]})
    return sorted(result, key=lambda item: item["area"], reverse=True)


def extract(path, target_height):
    source = Image.open(path).convert("RGBA")
    groups = components(source)
    substantial = [group for group in groups if group["area"] > 1000]
    if len(substantial) != 6:
        raise ValueError(f"{path.name}: expected six separate complete figures, found {len(substantial)}")
    groups = sorted(substantial, key=lambda item: item["bbox"][0])
    max_height = max(item["bbox"][3] - item["bbox"][1] for item in groups)
    max_width = max(item["bbox"][2] - item["bbox"][0] for item in groups)
    scale = min(target_height / max_height, 178 / max_width)
    frames = []
    for group in groups:
        left, top, right, bottom = group["bbox"]
        # Register from the boots, so head/hair sway does not get centered away.
        alpha = np.array(source.getchannel("A"))
        foot_y = bottom - max(3, round((bottom - top) * 0.09))
        ys, xs = np.where(alpha[foot_y:bottom, left:right] > 16)
        foot_x = left + (float(xs.min()) + float(xs.max()) + 1) / 2
        crop_left, crop_top = max(0, left - 2), max(0, top - 2)
        crop = source.crop((crop_left, crop_top, min(source.width, right + 2), min(source.height, bottom + 2)))
        crop = crop.resize(tuple(round(size * scale) for size in crop.size), Image.Resampling.LANCZOS)
        x = round(96 - (foot_x - crop_left) * scale)
        y = round(203 - (bottom - crop_top) * scale)
        frame = Image.new("RGBA", CELL)
        frame.alpha_composite(crop, (x, y))
        pixels = np.array(frame)
        pixels[pixels[:, :, 3] == 0, :3] = 0
        frame = Image.fromarray(pixels)
        bbox = frame.getchannel("A").point(lambda a: 255 if a > 16 else 0).getbbox()
        if not bbox or min(bbox[0], bbox[1], 192 - bbox[2], 208 - bbox[3]) < 2:
            raise ValueError("A fitted pose clips the safe cell margin")
        frames.append(frame)
    return frames, {"source_size": list(source.size), "pose_count": 6, "source_components": groups, "shared_row_scale": scale, "registration": "Shared row scale; planted boot anchors at x96 and baseline203; original upper-body displacement retained."}


def cells(image, row):
    return [image.crop((i * 192, row * 208, (i + 1) * 192, (row + 1) * 208)) for i in range(COUNTS[row])]


def motion_metrics(frames):
    arrays = [np.array(frame) for frame in frames]
    transitions = []
    for i, a in enumerate(arrays):
        b = arrays[(i + 1) % len(arrays)]
        visible = (a[:, :, 3] >= 128) | (b[:, :, 3] >= 128)
        changed = (np.abs(a.astype(np.int16) - b.astype(np.int16)).max(axis=2) > 20) & visible
        body = changed.copy()
        body[:105] = False
        body[184:] = False
        transitions.append({"from": i, "to": (i + 1) % len(arrays), "changed_visible_pixels": int(changed.sum()), "body_coat_arm_changed_pixels": int(body.sum())})
    normal = [step["changed_visible_pixels"] for step in transitions[:-1]]
    seam_ratio = transitions[-1]["changed_visible_pixels"] / max(1, float(np.median(normal)))
    return {"unique_frames": len({frame.tobytes() for frame in frames}), "transitions": transitions, "wrap_diff_over_median_step": seam_ratio, "note": "Pixel changes and seam ratios are measurements, not proof of animation appeal; visual review remains required."}


def inspect_atlas(image):
    if image.size != (1536, 2288) or image.mode != "RGBA":
        raise ValueError("Expected RGBA spriteVersionNumber2 atlas at1536x2288")
    for row, count in enumerate(COUNTS):
        for column in range(8):
            cell = image.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))
            bbox = cell.getchannel("A").getbbox()
            if bool(bbox) != (column < count):
                raise ValueError(f"Incorrect occupied/unused cell at row{row} column{column}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("atlas", "idle-strip", "thinking-strip", "output", "report"):
        parser.add_argument("--" + argument, type=Path, required=True)
    args = parser.parse_args()
    original = Image.open(args.atlas).convert("RGBA")
    inspect_atlas(original)
    output = original.copy()
    reports = {}
    target_height = max(frame.getchannel("A").point(lambda a: 255 if a > 16 else 0).getbbox()[3] - frame.getchannel("A").point(lambda a: 255 if a > 16 else 0).getbbox()[1] for frame in cells(original, 0))
    for state, path in (("idle", args.idle_strip), ("running", args.thinking_strip)):
        frames, geometry = extract(path, target_height)
        row = ROWS[state]
        output.paste((0, 0, 0, 0), (0, row * 208, 1536, (row + 1) * 208))
        for i, frame in enumerate(frames):
            output.paste(frame, (i * 192, row * 208))
        reports[state] = {"geometry": geometry, "before": motion_metrics(cells(original, row)), "after": motion_metrics(frames)}
        if reports[state]["after"]["unique_frames"] != 6:
            raise ValueError("Quiet loop contains repeated still frames")
        if reports[state]["after"]["wrap_diff_over_median_step"] > 1.5:
            raise ValueError("Loop wrap changes more than1.5x a normal step; inspect/repair source")
    unchanged = []
    for row in range(11):
        if row in ROWS.values():
            continue
        box = (0, row * 208, 1536, (row + 1) * 208)
        if original.crop(box).tobytes() != output.crop(box).tobytes():
            raise ValueError("Unrelated animation/gaze pixels changed")
        unchanged.append(row)
    inspect_atlas(output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output, optimize=True, compress_level=9)
    if Image.open(args.output).convert("RGBA").tobytes() != output.tobytes():
        raise ValueError("Lossless PNG parity failed")
    report = {"ok": True, "sprite_version": 2, "dimensions": list(output.size), "required_cells": 73, "transparent_unused_cells": 15, "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(), "encoded_bytes": args.output.stat().st_size, "before_encoded_bytes": args.atlas.stat().st_size, "unchanged_rows_pixel_exact": unchanged, "states": reports}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "states"}, indent=2))


if __name__ == "__main__":
    main()
