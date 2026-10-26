# Full-circle look-around loops

Continuous clockwise gaze motion: **up -> right -> down -> left -> up**, matching the original Look around animation.

These loops reuse all sixteen gaze poses directly from rows 9 and 10 of each package's original atlas. They preserve the original posture, proportions, natural head pitch/yaw and visible relaxed hands. No new artwork is generated.

| Action | Detailed | Simple |
| --- | --- | --- |
| Idle, 3.84 s | ![Detailed idle](hakase-detailed/idle.gif) | ![Simple idle](hakase-simple/idle.gif) |
| Thinking, 2.4 s | ![Detailed thinking](hakase-detailed/thinking.gif) | ![Simple thinking](hakase-simple/thinking.gif) |

Idle uses 240 ms per direction. Thinking uses 150 ms per direction, matching the original Look around preview. Both loop clockwise through all sixteen directions without reversing. The PNG frames are retained losslessly in each `frames` folder; GIFs use the existing export pipeline's shared palette and transparency threshold.

These are full sixteen-frame previews. The installable v2 pet format allocates six cells to each idle/thinking row, so these exact sixteen-frame loops cannot replace those rows within the current format. The pet-only installation tasks still use the existing native atlas animations. The sixteen directions remain available as the native gaze cells.

Validation checks the exact PNG source pixels, all sixteen GIF frames in order, shared-palette decoded pixels, alpha masks, frame durations, infinite looping and preservation of the source atlas. See each version's `validation.json` and `contact-sheet.png`.

Rebuild from the repository root with a Python environment containing Pillow:

```powershell
python -B pets/previews/circular-look-20261026/build_previews.py
```
