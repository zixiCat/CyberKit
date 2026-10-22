# CyberKit

Set up my Codex instructions and workflows on a new Windows computer with one task.

## Hakase desktop pets

Copy your chosen pet's task from the table into Codex to install only that design. The full Windows setup below is optional.

| Pet and motion preview | Copy into Codex (pet only) |
| --- | --- |
| **[Hakase (Detailed)](pets/hakase-detailed/README.md)**<br><img src="pets/hakase-detailed/animations/waving.gif" alt="Hakase (Detailed) waving" width="144" height="156"> | `Install only Hakase (Detailed). Follow the pet-only instructions at https://github.com/zixiCat/CyberKit/blob/main/pets/hakase-detailed/README.md. Skip the full Windows setup and preserve existing settings and other pets.` |
| **[Hakase (Simple)](pets/hakase-simple/README.md)**<br><img src="pets/hakase-simple/animations/waving.gif" alt="Hakase (Simple) waving" width="144" height="156"> | `Install only Hakase (Simple). Follow the pet-only instructions at https://github.com/zixiCat/CyberKit/blob/main/pets/hakase-simple/README.md. Skip the full Windows setup and preserve existing settings and other pets.` |

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
