# Build circular idle and thinking loops

`install_circular_loops.py` replaces each Hakase pet's idle row 0 and thinking/active-work row 7 (`running`) with approved clockwise gaze poses. The sequence is **Look01 → Look05 → Look07 → Look09 → Look13 → Look15 → Look01**: up → right → down-right → down → left → up-left → up.

The tool copies existing gaze cells exactly, keeping relaxed visible hands, original proportions and head turns. All sixteen gaze cells remain in rows 9 and 10. The other seven action rows are unchanged. No new artwork is needed for this revision.

The desktop app fixes idle and thinking at six frames each. Its idle cadence is `[1680, 660, 660, 840, 840, 1920]` milliseconds (6.6 seconds); thinking uses `[120, 120, 120, 120, 120, 220]` milliseconds (0.82 seconds). The native preview GIFs use these timings. The app may return to idle after a short thinking run, depending on its state. The [sixteen-frame references](../previews/circular-look-20261026/README.md) retain their separate 3.84-second idle and 2.4-second thinking pacing.

## Rebuild and validate

The builder copies the tracked `frames/look*.png` artwork from the sixteen-frame reference package. With no arguments, it updates both pets; `--pet hakase-simple` or `--pet hakase-detailed` selects one. Use `--verify` to check the repository packages without rewriting them.

```powershell
python -m pip install -r pets/tools/requirements.txt
python pets/tools/install_circular_loops.py
python pets/tools/install_circular_loops.py --verify
```

The builder checks the 1536 × 2288 v2 atlas, 73 occupied cells, 15 transparent unused cells, exact source-pose copies and preservation of the other rows. Reports are stored in each pet's `qa/circular-format.json`; `qa/circular-review.json` records the visual review.

Regenerate dependent previews with the package's `tools/export_previews.py --quiet-loops-only`, then run it with `--validate`. The quiet-loop option refreshes circular GIFs, contact sheets, showcase, preview and video while retaining the other seven native action GIFs. Check `animations/idle.gif`, `animations/running.gif`, the showcase and the idle-to-jump transition before installing.

```powershell
python -m pip install -r pets/hakase-detailed/tools/requirements.txt
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed --quiet-loops-only
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed --validate
```

Use the corresponding `hakase-simple` paths for the simple version.

## Install both pets

For a pet-only update:

```powershell
& ./setup/install-config.ps1 -RepositoryPath (Get-Location).Path -PetsOnly
```

`-PetsOnly` copies both pets' manifests and sprite sheets, backs up replacements, and preserves selection/configuration and other files. Refresh Settings > Pets after installing.

If the two pets are still installed under the earlier `cybercat` and `clover-detailed` folder names, add `-ReuseLegacyPetFolders`. When the corresponding Hakase folder is absent, the helper updates that existing folder in place with the current Hakase manifest and sheet. This preserves the selected folder and avoids creating duplicate pets. New installations continue to use the canonical `hakase-simple` and `hakase-detailed` folders.

## Separate tool for generated replacement strips

`replace_quiet_loops.py` remains available for future changes that require newly generated artwork. It fits six complete poses per row with one shared scale, registers planted boots and leaves other rows unchanged. Generate new artwork with the built-in ImageGen tool using the package's canonical design; this tool only fits existing pixels.

```powershell
python -m pip install -r pets/tools/requirements.txt
python pets/tools/replace_quiet_loops.py --atlas previous.png --idle-strip generated-idle.png --thinking-strip generated-thinking.png --output spritesheet.png --report quiet-loop-format.json
```
