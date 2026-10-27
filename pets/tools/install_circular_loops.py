"""Replace both native quiet-state rows with approved clockwise gaze pixels.

This packages existing artwork; it does not generate, redraw or rescale poses.
The sixteen-pose reference is sampled to the six slots the desktop player uses.
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

CELL = (192, 208)
COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)
POSES = (0, 4, 6, 8, 12, 14)
DIRECTIONS = ("up", "right", "down-right", "down", "left", "up-left")
TIMINGS = {"idle": [1680, 660, 660, 840, 840, 1920],
           "running": [120, 120, 120, 120, 120, 220]}
PETS = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cell(atlas, row, column):
    return atlas.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))


def inspect(atlas):
    if atlas.size != (1536, 2288) or atlas.mode != "RGBA":
        raise ValueError("Expected a 1536x2288 RGBA v2 spritesheet")
    for row, count in enumerate(COUNTS):
        for column in range(8):
            alpha = cell(atlas, row, column).getchannel("A")
            if bool(alpha.getbbox()) != (column < count):
                raise ValueError(f"Incorrect occupied/unused cell: {row}, {column}")


def build(pet, verify_only=False):
    package = PETS / pet
    source = package / "spritesheet.png"
    original_bytes = source.read_bytes()
    original = Image.open(source).convert("RGBA")
    inspect(original)
    reference = PETS / "previews/circular-look-20261026" / pet / "frames"
    looks = [Image.open(reference / f"look{i + 1:02}.png").convert("RGBA") for i in range(16)]
    for i, frame in enumerate(looks):
        if frame.size != CELL or frame.tobytes() != cell(original, 9 + i // 8, i % 8).tobytes():
            raise ValueError(f"Approved gaze reference differs at Look{i + 1:02}")
    frames = [looks[i] for i in POSES]
    if len({frame.tobytes() for frame in frames}) != 6:
        raise ValueError("Circular loop needs six distinct approved poses")
    output = original.copy()
    for row in (0, 7):
        output.paste((0, 0, 0, 0), (0, row * 208, 1536, (row + 1) * 208))
        for column, frame in enumerate(frames):
            output.paste(frame, (column * 192, row * 208))
    inspect(output)
    unchanged = [row for row in range(11) if row not in (0, 7)]
    for row in unchanged:
        box = (0, row * 208, 1536, (row + 1) * 208)
        if original.crop(box).tobytes() != output.crop(box).tobytes():
            raise ValueError(f"Unrelated row changed: {row}")
    if verify_only:
        if original.tobytes() != output.tobytes():
            raise ValueError("Installed atlas does not contain the approved circular loops")
        report = json.loads((package / "qa/circular-format.json").read_text(encoding="utf-8"))
        if report["sha256"] != digest(original_bytes):
            raise ValueError("Validation report is stale")
        return {"pet": pet, "ok": True, "sha256": report["sha256"], "verify_only": True}
    report_path = package / "qa/circular-format.json"
    previous = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
    previous_hash = digest(original_bytes)
    if previous.get("sha256") == previous_hash:
        previous_hash = previous["previous_atlas_sha256"]
    output.save(source, optimize=True, compress_level=9)
    encoded = Image.open(source).convert("RGBA")
    if encoded.tobytes() != output.tobytes():
        raise ValueError("Lossless PNG parity failed")
    report = {
        "ok": True, "sprite_version": 2, "dimensions": list(output.size),
        "required_cells": 73, "transparent_unused_cells": 15,
        "sha256": digest(source.read_bytes()), "encoded_bytes": source.stat().st_size,
        "previous_atlas_sha256": previous_hash,
        "unchanged_rows_pixel_exact": unchanged,
        "source_gaze_indices_zero_based": list(POSES),
        "source_look_names": [f"Look{i + 1:02}" for i in POSES],
        "directions": list(DIRECTIONS) + ["up"],
        "all_16_gaze_cells_preserved": True,
        "approved_pixels_exact": True, "new_artwork_generated": False,
        "states": {
            state: {"row_zero_based": row, "frames": 6, "durations_ms": TIMINGS[state],
                    "cycle_ms": sum(TIMINGS[state]), "loop_wrap": "up-left -> up"}
            for state, row in (("idle", 0), ("running", 7))
        },
        "timing_source": "Installed desktop app 26.1021.3705: idle base timings multiplied by six; running row seven timings unchanged.",
        "scope": "Twelve quiet-state cells replaced. Seven other action rows and all sixteen gaze poses remain pixel-identical.",
        "limitation": "Six native poses cannot reproduce the sixteen-pose reference's smoothness or its timing. Non-loop actions can return to idle after three cycles.",
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    atlas_report = {key: value for key, value in report.items() if key not in ("states", "limitation")}
    atlas_report["file"] = f"pets/{pet}/spritesheet.png"
    atlas_report["validator"] = "pets/tools/install_circular_loops.py"
    (package / "qa/atlas-validation.json").write_text(json.dumps(atlas_report, indent=2) + "\n", encoding="utf-8")
    provenance_path = package / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance.update(revision="native-circular-quiet-loops-20261027", sha256=report["sha256"],
                      encoded_bytes=report["encoded_bytes"], previous_atlas_sha256=previous_hash)
    provenance["quiet_loop_revision"] = {
        "tool": "Deterministic packaging of existing approved ImageGen gaze artwork",
        "states": ["idle", "running (thinking)"],
        "pose": "Gentle curious clockwise head roll, visible relaxed hands and planted boots.",
        "source_look_names": report["source_look_names"], "scope": report["scope"],
        "processing": "Exact 192x208 source cells copied without resizing or redrawing; lossless PNG encoding.",
        "review": "qa/circular-review.json", "format_validation": "qa/circular-format.json",
    }
    provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return {"pet": pet, "ok": True, "sha256": report["sha256"], "bytes": report["encoded_bytes"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pet", choices=("hakase-detailed", "hakase-simple"), action="append")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    print(json.dumps([build(pet, args.verify) for pet in args.pet or ("hakase-detailed", "hakase-simple")], indent=2))


if __name__ == "__main__":
    main()
