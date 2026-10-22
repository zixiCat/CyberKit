# Hakase (Detailed)

Hakase's detailed desktop pet. [Hakase (Simple)](../hakase-simple/README.md) is available separately.

## Motion previews

![Hakase (Detailed) blinking, waving, hopping and asking for input](cute.gif)

[All animations](preview.gif) · [Video](preview.mp4) · [Motion stills](motion-stills.png)

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

To rebuild exports from the checkout root:

```powershell
python -m pip install -r pets/hakase-detailed/tools/requirements.txt
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed
python pets/hakase-detailed/tools/export_previews.py --atlas pets/hakase-detailed/spritesheet.png --output-dir pets/hakase-detailed --validate
```

## Source and validation

The [canonical artwork](clover.png) reuses the exact full-resolution detailed illustration selected by the user. The [provenance](provenance.json) and [prompt set](source/prompts/README.md) describe the workflow. Every animation and gaze row was regenerated with built-in ImageGen from this detailed identity; incompatible frames from the simple version were not reused. Deterministic tools extract, register and compose generated pixels without drawing replacement artwork.

The second gaze strip needed one [uniform source-density fit](qa/source-density-normalization.json) of its entire eight-pose family. Both gaze rows then use the same recorded final registration scale; individual final cells are not resized separately.

Checks include [atlas validation](qa/atlas-validation.json), [quality gates](qa/pet-quality.json), [frame inspection](qa/frame-inspection.json), [state review](qa/standard-visual-review.json), [direction semantics](qa/direction-semantics.json), [continuity](qa/look-continuity.json), [three-reviewer blind gaze checks](qa/blind-validation.json), [independent visual review](qa/final-visual-review.json), [GIF timing/alpha validation](validation.json), and [both-design installer tests](qa/installer-test.json).

Any accepted intermediate gaze or hand-drawn variation is recorded in those reports. Visual tools inspect ordered native-size frames and contact sheets, rather than verifying live desktop playback. Working strips and revisions remain in the local creation run; private instructions, selection settings, credentials, sessions and histories are excluded from the package.
