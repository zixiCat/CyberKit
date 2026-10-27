# CyberKit

Set up my Codex instructions and workflows on a new Windows computer with one task.

## Hakase desktop pets

Copy your chosen pet's task from the table into Codex to install only that design. The full Windows setup below is optional.

Both installable pets now use a curious clockwise head roll for idle and thinking: **up → right → down → left → up**, with relaxed visible hands. The original quiet-state actions have been replaced in the pet packages.

| Circular motion | Detailed | Simple |
| --- | --- | --- |
| Circular idle · 6.6 s | <img src="pets/hakase-detailed/animations/idle.gif" alt="Hakase (Detailed) playing the installable circular idle poses" width="144" height="156"> | <img src="pets/hakase-simple/animations/idle.gif" alt="Hakase (Simple) playing the installable circular idle poses" width="144" height="156"> |
| Circular thinking · 0.82 s | <img src="pets/hakase-detailed/animations/running.gif" alt="Hakase (Detailed) playing the installable circular thinking poses" width="144" height="156"> | <img src="pets/hakase-simple/animations/running.gif" alt="Hakase (Simple) playing the installable circular thinking poses" width="144" height="156"> |

The installed loops use six selected poses from the approved sixteen-pose circle, matching the desktop app's fixed six-frame idle and thinking playback. The table shows those installed poses with the app's 6.6-second idle and 0.82-second thinking cadence. Thinking can return to idle after a short run, depending on the app state. The [full sixteen-frame references](pets/previews/circular-look-20261026/README.md) remain available for comparison; all sixteen original gaze cells are also retained in each pet.

| Pet and motion preview | Copy into Codex (pet only) |
| --- | --- |
| **[Hakase (Detailed)](pets/hakase-detailed/README.md)**<br><img src="pets/hakase-detailed/showcase.gif" alt="Hakase (Detailed) looking around clockwise, waving, hopping and waiting" width="144" height="156"> | `Install only Hakase (Detailed). Follow the pet-only instructions at https://github.com/zixiCat/CyberKit/blob/main/pets/hakase-detailed/README.md. Skip the full Windows setup and preserve existing settings and other pets.` |
| **[Hakase (Simple)](pets/hakase-simple/README.md)**<br><img src="pets/hakase-simple/showcase.gif" alt="Hakase (Simple) looking around clockwise, waving, hopping and waiting" width="144" height="156"> | `Install only Hakase (Simple). Follow the pet-only instructions at https://github.com/zixiCat/CyberKit/blob/main/pets/hakase-simple/README.md. Skip the full Windows setup and preserve existing settings and other pets.` |

The packages use `hakase-simple` and `hakase-detailed` folders. The full Windows setup installs both designs along with instructions and skills.

## Windows setup

Sign in to Codex or ChatGPT desktop on the new computer, then paste this task:

```text
Set up this Windows computer from https://github.com/zixiCat/CyberKit.

Fetch the latest main branch into a normal local checkout, reusing one if available and preserving uncommitted work. Review the repository instructions and setup scripts before running setup/install-config.ps1, passing the actual checkout root as RepositoryPath. Resolve this user's CODEX_HOME, Windows Documents folder and verified local skill directory; never reuse another computer's paths.

Install/update AGENTS.md, the custom skills, and both bundled Hakase desktop pets (Detailed and Simple). Preserve existing pet selection and unrelated pets; report the Settings > Pets > Refresh step when needed. Commit only shared instructions and Common hotwords to CyberKit. Keep the installed AGENTS.md's ### Local section only on this computer, preserve it during updates, and never copy it from another computer or upload it to GitHub. Preserve unrelated configuration and files. Never create worktrees or copy credentials/runtime state/sessions/local histories.

Read the installed skills and perform their bare-setup workflows: initialize this chat as the pinned manager with one quiet monitor that pauses when idle and resumes on new delegated work; check the available ActivityWatch service and its daily task; check reporting readiness. Use this computer as the default daily ActivityWatch scheduler at 20:00 Asia/Singapore without asking which computer owns it. Reuse matching local schedules, preserve existing settings and manual pauses, and leave other computers' jobs unchanged. Missing account-wide schedule listing must not block local setup. Match the manager monitor to this exact chat. Respect real account, plugin and installation prerequisites.

Do not reset existing setup, start reviews or publish Sites. If discovery needs a reload, complete available setup-helper steps first and report the exact remaining UI action. Finish with a brief verified ready/pending result.
```
