# Hakase (Detailed)

Hakase's detailed desktop pet. [Hakase (Simple)](../hakase-simple/README.md) is available separately.

## Approved circular motion

The new full-circle [idle and thinking previews](../previews/circular-look-20261026/README.md) reuse all sixteen original gaze poses: **up → right → down → left → up**, with relaxed visible hands and natural head turns.

| Idle · 3.84 s | Thinking · 2.4 s |
| --- | --- |
| ![Detailed circular idle](../previews/circular-look-20261026/hakase-detailed/idle.gif) | ![Detailed circular thinking](../previews/circular-look-20261026/hakase-detailed/thinking.gif) |

These previews retain sixteen frames. The native v2 idle and thinking rows each contain six cells, so the installation task below still uses the current native animations. See the linked preview package for source frames, validation and rebuild instructions.

## Current native motion previews

Idle and thinking now keep both hands naturally behind the lower back throughout, with relaxed shoulders, warm expressions, subtle breathing, body/head sway and hair/goggle/coat follow-through. Thinking uses glances and small nods while the hands stay hidden. Compare [idle before/after](qa/behind-back-idle-comparison.gif) and [thinking before/after](qa/behind-back-running-comparison.gif). The other seven action animations and all gaze cells remain pixel-identical, including the purposeful wave.

![Hakase (Detailed) blinking, waving, hopping and asking for input](showcase.gif)

An eight-second loop with short pauses between actions.

[All animations](preview.gif) · [Video](preview.mp4) · [Motion stills](motion-stills.png) · [Short loop](cute.gif)

| State | Preview |
| --- | --- |
| Hands behind back, breathing and sway | [idle.gif](animations/idle.gif) |
| Friendly wave | [waving.gif](animations/waving.gif) |
| Anticipation, hop and landing | [jumping.gif](animations/jumping.gif) |
| Expectant asking gesture | [waiting.gif](animations/waiting.gif) |
| Running right | [running-right.gif](animations/running-right.gif) |
| Running left | [running-left.gif](animations/running-left.gif) |
| Worried reaction and recovery | [failed.gif](animations/failed.gif) |
| Hands behind back, thoughtful tilt and glance | [running.gif](animations/running.gif) |
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

To rebuild exports from the checkout root (use `--showcase-only` to rebuild just the eight-second preview without FFmpeg):

```powershell
python -m pip install -r pets/hakase-detailed/tools/requirements.txt
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed --validate
```

## Source and validation

The [canonical artwork](clover.png) reuses the exact full-resolution detailed illustration selected by the user. The [provenance](provenance.json) and [prompt set](source/prompts/README.md) describe the workflow. Every animation and gaze row was regenerated with built-in ImageGen from this detailed identity; incompatible frames from the simple version were not reused. Deterministic tools extract, register and compose generated pixels without drawing replacement artwork.

The second gaze strip needed one [uniform source-density fit](qa/source-density-normalization.json) of its entire eight-pose family. Both gaze rows then use the same recorded final registration scale; individual final cells are not resized separately.

Current checks include [local atlas validation](qa/atlas-validation.json), [behind-back loop measurements](qa/behind-back-format.json), [pose and motion review](qa/behind-back-review.json), and [GIF timing/alpha validation](validation.json), and [duplicate-free in-place installer tests](qa/behind-back-installer.json). Prior generation reports are retained in [the history folder](qa/before-lively); the previous quiet-loop revision is saved under [before-behind-back](qa/before-behind-back). Gaze semantics and continuity reports apply to the pixel-identical gaze rows.

Any accepted intermediate gaze or hand-drawn variation is recorded in those reports. Visual tools inspect ordered native-size frames and contact sheets, rather than verifying live desktop playback. Working strips and revisions remain in the local creation run; private instructions, selection settings, credentials, sessions and histories are excluded from the package.

The [quiet-loop tooling guide](../tools/README.md) describes extraction, checks and updating both pets with `setup/install-config.ps1 -PetsOnly` while skipping instructions and skills. The standalone task above still installs only this pet. No frame counts or desktop timing settings were changed.

For computers still using the earlier installed folder names, `-PetsOnly -ReuseLegacyPetFolders` updates those existing pets in place with the current Hakase names, avoiding duplicates and preserving the selected folder. Fresh installations retain the canonical Hakase folders.
