# Clover (Detailed)

The saved detailed design keeps the user's chosen upper artwork: layered shaded green hair, oversized forehead goggles, an ivory coat with folded cuffs and lapels, a fitted wrap bodice and trimmed pleated skirt, and taller decorated boots. Its taller proportions and costume details are intentional. [Clover (Simple)](../cybercat/README.md) remains a separate saved pet.

## Motion previews

![Detailed Clover blinking, waving, hopping and asking for input](cute.gif)

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

## Install and choose

Run `setup/install-config.ps1` with the actual checkout root as `RepositoryPath`. It installs both designs, copying only each package's `pet.json` and `spritesheet.png` into the current user's resolved Codex home:

- `pets/clover-detailed`: **Clover (Detailed)**
- `pets/cybercat`: **Clover (Simple)**, retaining its existing folder for compatibility.

Open **Settings > Pets > Refresh**, then choose either version. Existing selection and unrelated pets stay intact. Replaced files are backed up locally; the earlier revision also remains in [Git history](https://github.com/zixiCat/CyberKit/tree/8633af6010bd2817b9c170f4b5b5215e488da608/pets/cybercat).

## Format and exports

The transparent lossless PNG uses sprite version 2: **1536 × 2288**, eight columns by eleven rows, with **192 × 208** cells. Nine animation states contain **57 frames** and two gaze rows contain **16 clockwise directions**. All fifteen unused cells are transparent. The detailed design is preserved through lossless PNG encoding; GIFs use a shared palette, no dithering, and alpha threshold 128 for clean small-size edges.

To rebuild exports from the checkout root:

```powershell
python -m pip install -r pets/clover-detailed/tools/requirements.txt
python pets/clover-detailed/tools/export_previews.py --atlas pets/clover-detailed/spritesheet.png --output-dir pets/clover-detailed
python pets/clover-detailed/tools/export_previews.py --atlas pets/clover-detailed/spritesheet.png --output-dir pets/clover-detailed --validate
```

## Source and validation

The [canonical artwork](clover.png) reuses the exact full-resolution detailed illustration selected by the user. The [provenance](provenance.json) and [prompt set](source/prompts/README.md) describe the workflow. Every animation and gaze row was regenerated with built-in ImageGen from this detailed identity; incompatible frames from the simple version were not reused. Deterministic tools extract, register and compose generated pixels without drawing replacement artwork.

The second gaze strip needed one [uniform source-density fit](qa/source-density-normalization.json) of its entire eight-pose family. Both gaze rows then use the same recorded final registration scale; individual final cells are not resized separately.

Checks include [atlas validation](qa/atlas-validation.json), [quality gates](qa/pet-quality.json), [frame inspection](qa/frame-inspection.json), [state review](qa/standard-visual-review.json), [direction semantics](qa/direction-semantics.json), [continuity](qa/look-continuity.json), [three-reviewer blind gaze checks](qa/blind-validation.json), [independent visual review](qa/final-visual-review.json), [GIF timing/alpha validation](validation.json), and [both-design installer tests](qa/installer-test.json).

Any accepted intermediate gaze or hand-drawn variation is recorded in those reports. Visual tools inspect ordered native-size frames and contact sheets, rather than verifying live desktop playback. Working strips and revisions remain in the local creation run; private instructions, selection settings, credentials, sessions and histories are excluded from the package.
