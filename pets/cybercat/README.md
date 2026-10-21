# Clover (Simple)

A compact green-haired scientist companion with oversized mint goggles, a simple ivory coat, and an evergreen outfit. The original simplified chibi design takes its green-hair/scientist cues from the user's visual reference; it does not assert an exact source-character identity.

This saved version keeps the simpler design. [Clover (Detailed)](../clover-detailed/README.md) retains the upper artwork's richer hair and costume details as a separate pet.

## Motion previews

![Clover blinking, waving, hopping and asking for input](cute.gif)

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

## Install

Run `setup/install-config.ps1` with the actual checkout root as `RepositoryPath`. It installs this package's `pet.json` and `spritesheet.png` into the current computer's resolved `CODEX_HOME/pets/cybercat`, alongside the separate detailed package. The existing folder name is retained for compatibility; the display name is **Clover (Simple)**. Existing selection and unrelated pets are preserved. Replaced files receive local backups.

Open **Settings > Pets > Refresh**, then choose **Clover (Simple)** or **Clover (Detailed)**. Desktop pets are local; these packages do not create account pets or copy another computer's selection.

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
