# CyberKit

Set up my Codex instructions and workflows on a new Windows computer with one task.

## Clover desktop pets

Both Clover designs are saved as separate green-haired scientist companions:

| Design | Artwork and animations | Motion |
| --- | --- | --- |
| **Clover (Detailed)** — layered hair, shaded coat and cuffs, trimmed pleated outfit, and taller boots | [Detailed version](pets/clover-detailed/README.md) | ![Detailed Clover waving](pets/clover-detailed/animations/waving.gif) |
| **Clover (Simple)** — rounded proportions, plain outfit, and simpler shapes | [Simple version](pets/cybercat/README.md) | ![Simple Clover waving](pets/cybercat/animations/waving.gif) |

The setup helper installs both packages into this computer's resolved Codex home. In Settings > Pets, select Refresh and choose either version. Existing pet selection and unrelated pets are preserved. The simple design retains the existing `cybercat` folder for compatibility; the detailed design uses `clover-detailed`.

## Windows setup

Sign in to Codex or ChatGPT desktop on the new computer, then paste this task:

```text
Set up this Windows computer from https://github.com/zixiCat/CyberKit.

Fetch the latest main branch into a normal local checkout, reusing one if available and preserving uncommitted work. Review the repository instructions and setup scripts before running setup/install-config.ps1, passing the actual checkout root as RepositoryPath. Resolve this user's CODEX_HOME, Windows Documents folder and verified local skill directory; never reuse another computer's paths.

Install/update AGENTS.md, the custom skills, and both bundled Clover desktop pets (Detailed and Simple). Preserve existing pet selection and unrelated pets; report the Settings > Pets > Refresh step when needed. Commit only shared instructions and Common hotwords to CyberKit. Keep the installed AGENTS.md's ### Local section only on this computer, preserve it during updates, and never copy it from another computer or upload it to GitHub. Preserve unrelated configuration and files. Never create worktrees or copy credentials/runtime state/sessions/local histories.

Read the installed skills and perform their bare-setup workflows: initialize this chat as the pinned manager with one quiet monitor that pauses when idle and resumes on new delegated work; check the available ActivityWatch service and its daily task; check reporting readiness. Use this computer as the default daily ActivityWatch scheduler at 20:00 Asia/Singapore without asking which computer owns it. Reuse matching local schedules, preserve existing settings and manual pauses, and leave other computers' jobs unchanged. Missing account-wide schedule listing must not block local setup. Match the manager monitor to this exact chat. Respect real account, plugin and installation prerequisites.

Do not reset existing setup, start reviews or publish Sites. If discovery needs a reload, complete available setup-helper steps first and report the exact remaining UI action. Finish with a brief verified ready/pending result.
```
