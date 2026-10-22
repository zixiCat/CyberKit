# Refresh idle and thinking loops

`replace_quiet_loops.py` fits six generated poses into the local desktop pet's idle row0 and thinking/active-work row7 (`running`). It uses one scale per source strip, registers planted boots, and leaves all other atlas rows pixel-identical. It checks73 occupied cells,15 transparent unused cells, safe fitted margins, six distinct frames and loop-wrap differences, then writes a losslessly compressed PNG and a measurement report. Visual review is still required; pixel differences do not prove appealing motion.

```powershell
python -m pip install -r pets/tools/requirements.txt
python pets/tools/replace_quiet_loops.py --atlas previous.png --idle-strip generated-idle.png --thinking-strip generated-thinking.png --output spritesheet.png --report quiet-loop-format.json
```

Generate replacement artwork with the built-in ImageGen tool, using each package's canonical design and accepted prompts. Recover complete separate poses; repair a strip if silhouettes touch. The tool fits existing artwork and never draws or invents replacement character pixels.

Regenerate dependent previews with the package's `tools/export_previews.py`. Preserve unrelated native GIFs when changing only quiet loops. Check the new `animations/idle.gif`, `animations/running.gif`, and both transitions before installing.

For a pet-only update, the reviewed setup helper can skip instructions and skills entirely:

```powershell
& ./setup/install-config.ps1 -RepositoryPath (Get-Location).Path -PetsOnly
```

The ordinary setup command retains its existing behavior. `-PetsOnly` copies only both pets' manifests and sprite sheets, backs up replacements, and preserves selection/configuration and other files. Refresh Settings > Pets after installing.

If the two pets are still installed under the earlier `cybercat` and `clover-detailed` folder names, add `-ReuseLegacyPetFolders`. When the corresponding Hakase folder is absent, the helper updates that existing folder in place with the current Hakase manifest and sheet. This preserves the selected folder and avoids creating duplicate pets. New installations continue to use the canonical `hakase-simple` and `hakase-detailed` folders.
