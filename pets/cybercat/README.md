# CyberCat

A simple purple cat-eared companion with cyan headphones, a halo, a plain hoodie, and a clean dark outline. Adapted from the [CyberCat brand mascot](https://github.com/zixiCat/CyberCat/tree/master/brand).

## Preview

![CyberCat blinking, waving, hopping and waiting](cute.gif)

[All animations](preview.gif) · [Video](preview.mp4) · [Motion stills](motion-stills.png)

## Animations

| Animation | Preview |
| --- | --- |
| Calm blinking | [idle.gif](animations/idle.gif) |
| Friendly wave | [waving.gif](animations/waving.gif) |
| Playful hop | [jumping.gif](animations/jumping.gif) |
| Hopeful waiting | [waiting.gif](animations/waiting.gif) |
| Running right | [running-right.gif](animations/running-right.gif) |
| Running left | [running-left.gif](animations/running-left.gif) |
| Error reaction | [failed.gif](animations/failed.gif) |
| Focused work | [running.gif](animations/running.gif) |
| Reviewing work | [review.gif](animations/review.gif) |

The desktop sprite sheet also includes sixteen clockwise look directions. See the [action contact sheet](contact-sheet.png), [look directions](look-directions.png), [look loop](look.gif), and [idle-to-jump transition](animations/idle-jump-idle.gif).

## Install

Run `setup/install-config.ps1` with the actual checkout root as `RepositoryPath`. It resolves this computer's Codex home and installs only `pet.json` and `spritesheet.png` into its `pets/cybercat` directory. Existing selection and unrelated pets stay unchanged; changed package files receive local backups. Then open Settings > Pets, select Refresh, and choose CyberCat.

The package uses sprite version 2: a transparent 1536 × 2288 PNG, eight columns and eleven rows, with 192 × 208 cells. The first nine rows contain 6, 8, 8, 4, 5, 8, 6, 6, and 6 animation frames; the last two rows contain sixteen look directions. Unused cells are transparent.

## Clean animation exports

The PNG keeps smooth alpha edges. Native-size GIFs use a shared palette, no dithering, and a reserved transparent color. Pixels below alpha 128 remain transparent, preventing faint edge pixels from becoming a speckled opaque border.

To rebuild previews from the sprite sheet, run these commands from the checkout root:

```powershell
python -m pip install -r pets/cybercat/tools/requirements.txt
python pets/cybercat/tools/export_previews.py --atlas pets/cybercat/spritesheet.png --output-dir pets/cybercat
python pets/cybercat/tools/export_previews.py --atlas pets/cybercat/spritesheet.png --output-dir pets/cybercat --validate
```

## Validation

The [atlas validation](qa/atlas-validation.json) and [quality gate](qa/pet-quality.json) passed for the packaged PNG. The [GIF validation](validation.json) confirms exact timing and zero alpha-mask mismatches for all 57 state frames, the cute sequence, and the idle-to-jump transition.

The [three-reviewer blind gaze check](qa/blind-validation.json) passed the four cardinal directions. The 157.5° pose is nearly down-facing; its slight rightward component is difficult to distinguish by itself. This and other subtle intermediate gaze steps are recorded in the [visual review](qa/direction-semantics.json). Halo openings are intentional transparent gaps. The jump returns to the idle baseline.

Reports describe generation-time checks. Intermediate strips and frames remain outside this repository; local paths in packaged reports are normalized.

## Source and generation

The original mascot reference is [source/CyberCat.png](source/CyberCat.png), from CyberCat commit `d85444aec918b33c9418af0953f552e8491bac21`. The simplified full-body design is [cybercat.png](cybercat.png). Built-in ImageGen produced the character and pose strips with transparent backgrounds; deterministic tools extracted frames, aligned each state, assembled the sprite sheet, and encoded previews.

The [generation brief and provenance](provenance.json) preserve the purple/cyan identity while replacing tiny costume details and highlights with broad shapes and a consistent outline. Local pet selection, account data, sessions, and histories do not belong in this directory.
