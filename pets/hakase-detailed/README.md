# Hakase (Detailed)

Hakase's detailed desktop pet. [Hakase (Simple)](../hakase-simple/README.md) is available separately.

## Circular idle and thinking

Both quiet states now use the approved curious head roll with relaxed visible hands: **up → right → down → left → up**. The installable spritesheet replaces the earlier hands-behind-back idle and thinking actions.

| Native circular idle · 6.6 s | Native circular thinking · 0.82 s |
| --- | --- |
| ![Detailed native circular idle](animations/idle.gif) | ![Detailed native circular thinking](animations/running.gif) |

The desktop app plays six frames in each of these states. The installed sequence selects **Look01 → Look05 → Look07 → Look09 → Look13 → Look15 → Look01** from the approved circle: up → right → down-right → down → left → up-left → up. Each selected pose keeps the original artwork exactly. The GIFs use the app's 6.6-second idle and 0.82-second thinking cadence. Thinking can return to idle after a short run, depending on the app state. The [full sixteen-frame reference](../previews/circular-look-20261026/README.md) remains available separately; all sixteen native gaze cells are retained.

## Motion previews

![Hakase (Detailed) looking around clockwise, waving, hopping and asking for input](showcase.gif)

The 10.72-second showcase combines circular idle and thinking with a friendly wave, hop and waiting gesture. The other seven action animations keep their existing poses.

[All animations](preview.gif) · [Video](preview.mp4) · [Motion stills](motion-stills.png) · [Short loop](cute.gif)

| State | Preview |
| --- | --- |
| Circular idle, relaxed visible hands | [idle.gif](animations/idle.gif) |
| Friendly wave | [waving.gif](animations/waving.gif) |
| Anticipation, hop and landing | [jumping.gif](animations/jumping.gif) |
| Expectant asking gesture | [waiting.gif](animations/waiting.gif) |
| Running right | [running-right.gif](animations/running-right.gif) |
| Running left | [running-left.gif](animations/running-left.gif) |
| Worried reaction and recovery | [failed.gif](animations/failed.gif) |
| Circular thinking, relaxed visible hands | [running.gif](animations/running.gif) |
| Inspecting and approving work | [review.gif](animations/review.gif) |

See the [contact sheet](contact-sheet.png), [sixteen gaze directions](look-directions.png), [gaze loop](look.gif), and [idle-to-jump transition](animations/idle-jump-idle.gif).

## Copy and use only this pet

Copy this task into Codex to install **Hakase (Detailed)** without the full Windows setup:

```text
Install only Hakase (Detailed) from https://github.com/zixiCat/CyberKit, using the latest main branch.

Resolve this computer's CODEX_HOME (default: .codex in the current user's home folder). Copy only pets/hakase-detailed/pet.json and pets/hakase-detailed/spritesheet.png from the repository into CODEX_HOME/pets/hakase-detailed/, keeping those filenames. Back up any existing files before replacing them and verify the installed files match the source.

Do not run setup/install-config.ps1 or perform the Windows setup. Leave AGENTS.md, skills, schedules, other pets, and the existing pet selection unchanged. Never create worktrees or copy credentials/runtime state. Finish by telling me to open Settings > Pets > Refresh and choose Hakase (Detailed).
```

For both pets plus instructions and skills, use the separate [full Windows setup](../../README.md#windows-setup). The earlier revision remains in [Git history](https://github.com/zixiCat/CyberKit/tree/8633af6010bd2817b9c170f4b5b5215e488da608/pets/cybercat).

## Format and exports

The transparent lossless PNG uses sprite version 2: **1536 × 2288**, eight columns by eleven rows, with **192 × 208** cells. Nine animation states contain **57 frames** and two gaze rows contain **16 clockwise directions**. All fifteen unused cells are transparent. The detailed design is preserved through lossless PNG encoding; GIFs use a shared palette, no dithering, and alpha threshold 128 for clean small-size edges.

To rebuild exports from the checkout root (use `--quiet-loops-only` to refresh circular-loop exports while retaining other action GIFs, or `--showcase-only` for just the showcase without FFmpeg):

```powershell
python -m pip install -r pets/hakase-detailed/tools/requirements.txt
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed --validate
```

## Source and validation

The [canonical artwork](clover.png) reuses the exact full-resolution detailed illustration selected by the user. The [provenance](provenance.json) and [prompt set](source/prompts/README.md) describe the workflow. The original animation and gaze artwork was generated with built-in ImageGen from this detailed identity; incompatible frames from the simple version were not reused. The current circular loops copy selected approved gaze cells into idle and thinking without redrawing or resizing them. Deterministic tools extract, register and compose generated pixels without drawing replacement artwork.

The second gaze strip needed one [uniform source-density fit](qa/source-density-normalization.json) of its entire eight-pose family. Both gaze rows then use the same recorded final registration scale; individual final cells are not resized separately.

Current checks include [local atlas validation](qa/atlas-validation.json), [circular-loop measurements](qa/circular-format.json), [circular pose and motion review](qa/circular-review.json), and [GIF timing/alpha validation](validation.json). Earlier generation and hands-behind-back reports describe historical revisions only. Gaze semantics and continuity reports still apply to the unchanged gaze rows.

Any accepted intermediate gaze or hand-drawn variation is recorded in those reports. Visual tools inspect ordered native-size frames and contact sheets, rather than verifying live desktop playback. Working strips and revisions remain in the local creation run; private instructions, selection settings, credentials, sessions and histories are excluded from the package.

The [circular-loop tooling guide](../tools/README.md) describes pose selection, checks and updating both pets with `setup/install-config.ps1 -PetsOnly` while skipping instructions and skills. The standalone task above still installs only this pet. No frame counts or desktop timing settings were changed.

For computers still using the earlier installed folder names, `-PetsOnly -ReuseLegacyPetFolders` updates those existing pets in place with the current Hakase names, avoiding duplicates and preserving the selected folder. Fresh installations retain the canonical Hakase folders.
