# Hakase (Simple)

Hakase's simple desktop pet. [Hakase (Detailed)](../clover-detailed/README.md) is available separately.

## Motion previews

![Hakase (Simple) blinking, waving, hopping and asking for input](cute.gif)

[All states](preview.gif) · [Video](preview.mp4) · [Motion stills](motion-stills.png)

| State | Preview |
| --- | --- |
| Calm breathing and blink | [idle.gif](animations/idle.gif) |
| Friendly wave | [waving.gif](animations/waving.gif) |
| Anticipation, hop and landing | [jumping.gif](animations/jumping.gif) |
| Expectant asking gesture | [waiting.gif](animations/waiting.gif) |
| Running right | [running-right.gif](animations/running-right.gif) |
| Running left | [running-left.gif](animations/running-left.gif) |
| Worried reaction and recovery | [failed.gif](animations/failed.gif) |
| Active thinking | [running.gif](animations/running.gif) |
| Inspecting and approving work | [review.gif](animations/review.gif) |

The [action contact sheet](contact-sheet.png), [sixteen gaze directions](look-directions.png), [gaze loop](look.gif), and [idle-to-jump transition](animations/idle-jump-idle.gif) show the complete pose set. Head, eyes, goggles and hair follow the gaze while the torso and boots remain planted.

## Copy and use only this pet

Copy this task into Codex to install **Hakase (Simple)** without the full Windows setup:

```text
Install only Hakase (Simple) from https://github.com/zixiCat/CyberKit, using the latest main branch.

Resolve this computer's CODEX_HOME (default: .codex in the current user's home folder). Copy only pets/cybercat/pet.json and pets/cybercat/spritesheet.png from the repository into CODEX_HOME/pets/cybercat/, keeping those filenames. Back up any existing files before replacing them and verify the installed files match the source.

Do not run setup/install-config.ps1 or perform the Windows setup. Leave AGENTS.md, skills, schedules, other pets, and the existing pet selection unchanged. Never create worktrees or copy credentials/runtime state. Finish by telling me to open Settings > Pets > Refresh and choose Hakase (Simple).
```

The existing `cybercat` folder name is retained for compatibility; the display name is **Hakase (Simple)**. Desktop pets are local; this package does not create an account pet or copy another computer's selection. For both pets plus instructions and skills, use the separate [full Windows setup](../../README.md#windows-setup).

The former design remains recoverable in [Git history](https://github.com/zixiCat/CyberKit/tree/474abe00db648ac27d8f470d0fbc090f8474a55a/pets/cybercat) and in the local backups made during replacement.

## Format and exports

The transparent, losslessly encoded PNG is sprite version 2: **1536 × 2288**, eight columns and eleven rows, with **192 × 208** cells. Nine animation rows contain **57 frames**; two gaze rows contain **16 clockwise directions**. All fifteen unused cells remain transparent.

The PNG preserves smooth alpha edges. Native-size GIFs use a shared palette, no dithering, and a reserved transparent index; an alpha threshold of 128 keeps faint edge pixels from becoming speckled opaque borders.

To rebuild and check the exports from the checkout root:

```powershell
python -m pip install -r pets/cybercat/tools/requirements.txt
python pets/cybercat/tools/export_previews.py --atlas pets/cybercat/spritesheet.png --output-dir pets/cybercat
python pets/cybercat/tools/export_previews.py --atlas pets/cybercat/spritesheet.png --output-dir pets/cybercat --validate
```

## Evidence and source

The [provenance](provenance.json), [canonical design](clover.png), and [accepted prompt set](source/prompts/README.md) describe the artwork. Built-in ImageGen produced the base and every state/gaze strip; deterministic tools extracted connected poses, applied a uniform registration per row, composed the atlas, and encoded previews. Both running directions were generated separately.

The [atlas validator](qa/atlas-validation.json), [quality gate](qa/pet-quality.json), [standard-frame inspection](qa/frame-inspection.json), [visual review](qa/standard-visual-review.json), [direction semantics](qa/direction-semantics.json), [continuity analysis](qa/look-continuity.json), and [blind direction check](qa/blind-validation.json) record the checks on this revision. [GIF validation](validation.json) checks the exact timing and alpha masks of all 57 standard frames and the combined transitions.

Visual inspection uses ordered native-size frames and contact sheets; a still-image inspection tool does not verify live playback. The largest gaze step is 157.5° to 180°; 202.5° and 225° are close in appearance. Subtle intermediate gaze components and minor hand-drawn hair/outline variation are documented in the reviews. Reports describe generation-time checks and use repository-relative paths. Intermediate source strips, rejected revisions and working frames remain in the local creation run; credentials, selections, local instructions and runtime histories are excluded.
