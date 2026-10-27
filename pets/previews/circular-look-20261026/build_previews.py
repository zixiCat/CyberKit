"""Replay all 16 approved gaze poses in clockwise order without redrawing them."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image, ImageSequence

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PETS = HERE.parents[1]
spec = importlib.util.spec_from_file_location("export", PETS / "hakase-detailed/tools/export_previews.py")
export = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export)
CADENCES = {"idle": 240, "thinking": 150}
summary = []
for pet in ("hakase-detailed", "hakase-simple"):
    source = PETS / pet / "spritesheet.png"
    original_bytes = source.read_bytes()
    atlas = Image.open(source).convert("RGBA")
    frames = [
        atlas.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))
        for row in (9, 10) for column in range(8)
    ]
    assert len(frames) == 16 and all(f.getchannel("A").getbbox() for f in frames)
    destination = HERE / pet
    frame_directory = destination / "frames"
    frame_directory.mkdir(parents=True, exist_ok=True)
    for number, frame in enumerate(frames, 1):
        path = frame_directory / f"look{number:02}.png"
        frame.save(path, optimize=True)
        assert Image.open(path).convert("RGBA").tobytes() == frame.tobytes()
    palette = export.make_palette(frames)
    expected = [export.indexed_frame(frame, palette).convert("RGBA") for frame in frames]
    checks = {}
    for action, milliseconds in CADENCES.items():
        durations = [milliseconds] * 16
        path = destination / f"{action}.gif"
        export.save_gif(frames, durations, path, palette)
        result = export.validate_gif(frames, durations, path)
        with Image.open(path) as gif:
            actual = [f.convert("RGBA") for f in ImageSequence.Iterator(gif)]
            assert gif.info.get("loop") == 0
        assert all(a.tobytes() == b.tobytes() for a, b in zip(actual, expected))
        checks[action] = {
            **result,
            "source_frame_order": list(range(1, 17)),
            "clockwise_degrees": [22.5 * i for i in range(16)],
            "frame_ms": milliseconds,
            "loop_ms": sum(durations),
            "palette_pixels_exact": True,
            "infinite_loop": True,
        }
    export.save_look_sheet(frames, destination / "contact-sheet.png")
    assert source.read_bytes() == original_bytes
    report = {
        "ok": True,
        "preview_only": True,
        "artwork": "Exact original approved gaze-cell pixels; no new artwork generated.",
        "source_atlas": f"../../../{pet}/spritesheet.png",
        "source_atlas_sha256": hashlib.sha256(original_bytes).hexdigest(),
        "source_rows_zero_indexed": [9, 10],
        "source_png_frames_pixel_exact": True,
        "direction": "up -> right -> down -> left -> up",
        "original_package_unchanged": True,
        "exports": checks,
        "native_idle_thinking_row_cells": 6,
        "native_selected_gaze_indices_zero_based": [0, 4, 6, 8, 12, 14],
        "native_installation": "The Hakase packages now use six selected clockwise poses in idle and thinking. These full sixteen-frame references retain the original smooth motion and independent preview timing.",
    }
    (destination / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary.append({"pet": pet, "ok": True, "previews": {a: str(destination / f"{a}.gif") for a in CADENCES}})
print(json.dumps(summary, indent=2))
