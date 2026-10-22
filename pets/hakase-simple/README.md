# Hakase (Simple)

Hakase's simple desktop pet. [Hakase (Detailed)](../hakase-detailed/README.md) is available separately.

## Motion previews

Idle and thinking were refreshed with gentle torso/head sway, breathing, hair/goggle/coat follow-through and low relaxed resting hands. Thinking has one brief chin gesture and returns both hands down. Compare [idle before/after](qa/quiet-idle-comparison.gif) and [thinking before/after](qa/quiet-running-comparison.gif). The other seven animations and all gaze cells remain pixel-identical.

![Hakase (Simple) blinking, waving, hopping and asking for input](showcase.gif)

An eight-second loop with short pauses between actions.

[All states](preview.gif) · [Video](preview.mp4) · [Motion stills](motion-stills.png) · [Short loop](cute.gif)

| State | Preview |
| --- | --- |
| Breathing, soft sway and blink | [idle.gif](animations/idle.gif) |
| Friendly wave | [waving.gif](animations/waving.gif) |
| Anticipation, hop and landing | [jumping.gif](animations/jumping.gif) |
| Expectant asking gesture | [waiting.gif](animations/waiting.gif) |
| Running right | [running-right.gif](animations/running-right.gif) |
| Running left | [running-left.gif](animations/running-left.gif) |
| Worried reaction and recovery | [failed.gif](animations/failed.gif) |
| Thoughtful sway and brief chin gesture | [running.gif](animations/running.gif) |
| Inspecting and approving work | [review.gif](animations/review.gif) |

The [action contact sheet](contact-sheet.png), [sixteen gaze directions](look-directions.png), [gaze loop](look.gif), and [idle-to-jump transition](animations/idle-jump-idle.gif) show the complete pose set. Head, eyes, goggles and hair follow the gaze while the torso and boots remain planted.

## Copy and use only this pet

Copy this task into Codex to install **Hakase (Simple)** without the full Windows setup:

```text
Install only Hakase (Simple) from https://github.com/zixiCat/CyberKit, using the latest main branch.

Resolve this computer's CODEX_HOME (default: .codex in the current user's home folder). Copy only pets/hakase-simple/pet.json and pets/hakase-simple/spritesheet.png from the repository into CODEX_HOME/pets/hakase-simple/, keeping those filenames. Back up any existing files before replacing them and verify the installed files match the source.

Do not run setup/install-config.ps1 or perform the Windows setup. Leave AGENTS.md, skills, schedules, other pets, and the existing pet selection unchanged. Never create worktrees or copy credentials/runtime state. Finish by telling me to open Settings > Pets > Refresh and choose Hakase (Simple).
```

The package installs into `pets/hakase-simple`; its display name is **Hakase (Simple)**. Desktop pets are local; this package does not create an account pet or copy another computer's selection. For both pets plus instructions and skills, use the separate [full Windows setup](../../README.md#windows-setup).

The former design remains recoverable in [Git history](https://github.com/zixiCat/CyberKit/tree/474abe00db648ac27d8f470d0fbc090f8474a55a/pets/cybercat) and in the local backups made during replacement.

## Format and exports

The transparent, losslessly encoded PNG is sprite version 2: **1536 × 2288**, eight columns and eleven rows, with **192 × 208** cells. Nine animation rows contain **57 frames**; two gaze rows contain **16 clockwise directions**. All fifteen unused cells remain transparent.

The PNG preserves smooth alpha edges. Native-size GIFs use a shared palette, no dithering, and a reserved transparent index; an alpha threshold of 128 keeps faint edge pixels from becoming speckled opaque borders.

To rebuild and check the exports from the checkout root (use `--showcase-only` to rebuild just the eight-second preview without FFmpeg):

```powershell
python -m pip install -r pets/hakase-simple/tools/requirements.txt
python pets/hakase-simple/tools/export_previews.py --atlas pets/hakase-simple/spritesheet.png --output-dir pets/hakase-simple
python pets/hakase-simple/tools/export_previews.py --atlas pets/hakase-simple/spritesheet.png --output-dir pets/hakase-simple --validate
```

## Evidence and source

The [provenance](provenance.json), [canonical design](clover.png), and [accepted prompt set](source/prompts/README.md) describe the artwork. Built-in ImageGen produced the base and every state/gaze strip; deterministic tools extracted connected poses, applied a uniform registration per row, composed the atlas, and encoded previews. Both running directions were generated separately.

Current checks include [local atlas validation](qa/atlas-validation.json), [quiet-loop measurements](qa/quiet-loop-format.json), [visual review](qa/quiet-loop-review.json), and [GIF timing/alpha validation](validation.json). Prior generation reports are retained in [the history folder](qa/before-lively). Gaze semantics and continuity reports apply to the pixel-identical gaze rows.

Visual inspection uses ordered native-size frames and contact sheets; a still-image inspection tool does not verify live playback. The largest gaze step is 157.5° to 180°; 202.5° and 225° are close in appearance. Subtle intermediate gaze components and minor hand-drawn hair/outline variation are documented in the reviews. Reports describe generation-time checks and use repository-relative paths. Intermediate source strips, rejected revisions and working frames remain in the local creation run; credentials, selections, local instructions and runtime histories are excluded.

The [quiet-loop tooling guide](../tools/README.md) describes extraction, checks and updating both pets with `setup/install-config.ps1 -PetsOnly` while skipping instructions and skills. The standalone task above still installs only this pet. No frame counts or desktop timing settings were changed.
