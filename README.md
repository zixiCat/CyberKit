# CyberKit

Set up my Codex instructions and workflows on a new Windows computer with one task.

## Clover desktop pets

Both Clover designs are saved as separate green-haired scientist companions:

| Design | Artwork and animations | Motion |
| --- | --- | --- |
| **Clover (Detailed)** — layered hair, shaded coat and cuffs, trimmed pleated outfit, and taller boots | [Detailed version](pets/clover-detailed/README.md) | ![Detailed Clover waving](pets/clover-detailed/animations/waving.gif) |
| **Clover (Simple)** — rounded proportions, plain outfit, and simpler shapes | [Simple version](pets/cybercat/README.md) | ![Simple Clover waving](pets/cybercat/animations/waving.gif) |

### Copy and use one pet

Want just a pet? Copy the task for your chosen design into Codex. Each task installs only that pet; the full Windows setup below is optional.

**Clover (Detailed)**

```text
Install only Clover (Detailed) from https://github.com/zixiCat/CyberKit, using the latest main branch.

Resolve this computer's CODEX_HOME (default: .codex in the current user's home folder). Copy only pets/clover-detailed/pet.json and pets/clover-detailed/spritesheet.png from the repository into CODEX_HOME/pets/clover-detailed/, keeping those filenames. Back up any existing files before replacing them and verify the installed files match the source.

Do not run setup/install-config.ps1 or perform the Windows setup. Leave AGENTS.md, skills, schedules, other pets, and the existing pet selection unchanged. Never create worktrees or copy credentials/runtime state. Finish by telling me to open Settings > Pets > Refresh and choose Clover (Detailed).
```

**Clover (Simple)**

```text
Install only Clover (Simple) from https://github.com/zixiCat/CyberKit, using the latest main branch.

Resolve this computer's CODEX_HOME (default: .codex in the current user's home folder). Copy only pets/cybercat/pet.json and pets/cybercat/spritesheet.png from the repository into CODEX_HOME/pets/cybercat/, keeping those filenames. Back up any existing files before replacing them and verify the installed files match the source.

Do not run setup/install-config.ps1 or perform the Windows setup. Leave AGENTS.md, skills, schedules, other pets, and the existing pet selection unchanged. Never create worktrees or copy credentials/runtime state. Finish by telling me to open Settings > Pets > Refresh and choose Clover (Simple).
```

The simple design retains the existing `cybercat` folder for compatibility; the detailed design uses `clover-detailed`. The full Windows setup installs both designs along with instructions and skills.

## Windows setup

Sign in to Codex or ChatGPT desktop on the new computer, then paste this task:

```text
Set up this Windows computer from https://github.com/zixiCat/CyberKit.

Fetch the latest main branch into a normal local checkout, reusing one if available and preserving uncommitted work. Review the repository instructions and setup scripts before running setup/install-config.ps1, passing the actual checkout root as RepositoryPath. Resolve this user's CODEX_HOME, Windows Documents folder and verified local skill directory; never reuse another computer's paths.

Install/update AGENTS.md, the custom skills, and both bundled Clover desktop pets (Detailed and Simple). Preserve existing pet selection and unrelated pets; report the Settings > Pets > Refresh step when needed. Commit only shared instructions and Common hotwords to CyberKit. Keep the installed AGENTS.md's ### Local section only on this computer, preserve it during updates, and never copy it from another computer or upload it to GitHub. Preserve unrelated configuration and files. Never create worktrees or copy credentials/runtime state/sessions/local histories.

Read the installed skills and perform their bare-setup workflows: initialize this chat as the pinned manager with one quiet monitor that pauses when idle and resumes on new delegated work; check the available ActivityWatch service and its daily task; check reporting readiness. Use this computer as the default daily ActivityWatch scheduler at 20:00 Asia/Singapore without asking which computer owns it. Reuse matching local schedules, preserve existing settings and manual pauses, and leave other computers' jobs unchanged. Missing account-wide schedule listing must not block local setup. Match the manager monitor to this exact chat. Respect real account, plugin and installation prerequisites.

Do not reset existing setup, start reviews or publish Sites. If discovery needs a reload, complete available setup-helper steps first and report the exact remaining UI action. Finish with a brief verified ready/pending result.
```
