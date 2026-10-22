# New Windows computer: install once, invoke each skill

The repository carries reusable instructions and helpers. Login and a skill copy do not establish that old local chats, jobs, histories or permissions are available on this computer. ActivityWatch histories and task-tracking records stay on their original device; the new computer starts fresh.

## Install once

1. Install the current Codex desktop app and sign in to the account/workspace that owns the existing Sites. Obtain private GitHub access to `zixiCat/CyberKit`. Clone a normal checkout or download its source; never create a worktree. Skills cannot install themselves before Codex discovers them.
2. Ask Codex to verify the user skill directory scanned by this installed desktop build. This audited desktop exposes custom skills in `CODEX_HOME/skills` (default `.codex/skills`); current [published skill-discovery docs](https://learn.chatgpt.com/docs/build-skills) also describe `.agents/skills` user/repository locations. Do not assume the old app's location or install duplicates into both. In PowerShell at the checkout root, run the bundled installer below, or ask Codex to run it. It resolves `CODEX_HOME` or the current user's `.codex` for `AGENTS.md`, defaults skills to that home's `skills`, and accepts `-SkillsPath <verified-absolute-user-skill-directory>` when the target build scans a different location. It backs up replaced instruction/skill files locally, skips private runtime artifacts, preserves other skills/configuration, and is safe to repeat. Review the repository/helper before running it. If PowerShell policy or a security prompt blocks it, use the supported trust/review flow; do not weaken global policy.

```powershell
& .\setup\install-config.ps1 -RepositoryPath (Get-Location).Path
```

3. Reopen a chat so the installed skills appear. Check active instructions: an existing `AGENTS.override.md` can take precedence over `AGENTS.md`; preserve and reconcile it deliberately. Enable/connect needed plugins/tools through their normal account and permission flows. The custom skills do not bundle Browser, Sites, app scheduling/thread tools, runtime dependencies, or account credentials. A missing capability must be reported, not simulated.

## Shared and local AGENTS.md instructions

`ChatGPT/.codex/AGENTS.md` in GitHub contains shared instructions and `### Common` hotwords only. The installed `AGENTS.md` may also have a `### Local` section for this computer's hotwords. Keep that section only on this computer; never commit or upload it, and never seed a new computer with another computer's Local section. When syncing installed instructions back to CyberKit, exclude the entire Local section through the next heading of level three or higher (or the end of the file).

The installer preserves an existing Local section while updating shared instructions and Common hotwords. A fresh installation receives only the shared content. Repeated installs preserve Local without duplicating it. Review the staged diff before every sync to verify that no Local section or its hotwords were included.

## Then select the skill and press Enter

The helper also installs both saved Hakase designs: `pets/hakase-simple` becomes `<resolved CODEX_HOME>/pets/hakase-simple` (**Hakase (Simple)**), and `pets/hakase-detailed` becomes `<resolved CODEX_HOME>/pets/hakase-detailed` (**Hakase (Detailed)**). Each installs only `pet.json` and `spritesheet.png`. It preserves unrelated pet files and existing selection, and backs up changed package files before replacing them. These are portable artwork and metadata, not another computer's pet settings or runtime state. Open Settings > Pets, select Refresh, and choose either version. Preview the reusable GIFs and source notes in the [simple guide](../pets/hakase-simple/README.md) or [detailed guide](../pets/hakase-detailed/README.md). Installing these finished assets does not require regenerating the pets or installing a creation skill.

| Bare invocation | What it initializes/checks | What still needs a decision or local prerequisite |
| --- | --- | --- |
| `$activitywatch-life-review` | Local browser access, current host/watcher evidence, daily task reused/created on this computer without an ownership question | Install/start ActivityWatch and relevant browser watcher through their official flows; grant permissions yourself where needed. Empty history is expected on a fresh device. |
| `$task-manager` | Rename/pin the current chat; one matching quiet two-minute monitor, PAUSED with no executable work, and identity-bound local registry | Reuse/resume the same idle-paused monitor on actual new delegations. Honor explicit manual pauses. A copied skill does not restore old delegations; ambiguous old monitor ownership needs resolution. |
| `$personal-work-report` | Runtime/template checks and Documents `Codex\WorkReports`; optional existing hub access check | Local drafting works independently of Sites. Connect Sites for requested publication; retrieve matching source only when needed. No report or schedule is invented. |

Explicit reviews/report requests still perform that work. Scheduled review and monitor prompts keep their own modes. A setup check reports readiness or the precise remaining item without requiring extra setup words.

## Where state belongs

Existing Site addresses:

| Site | Current address | Existing project ID |
| --- | --- | --- |
| WorkReport | [report.zixicat.chatgpt.site](https://report.zixicat.chatgpt.site) | `appgprj_6acfb9f7b04c819181711de6615b683f` |
| EnglishMemoryCard | [en.zixicat.chatgpt.site](https://en.zixicat.chatgpt.site) | `appgprj_6acd95dec3f48191847acedea3d2f91a` |

These address mappings were verified with native read-only `get_site`: both projects are active and owner-private. Recheck the same project ID, `current_live_url` and account/access before use; do not rename a Site, change its domain/audience or deploy it during setup. EnglishMemoryCard uses its existing project workflow; this repository does not bundle a dedicated English skill. No Site content or learning history is copied as part of these references.

| Item | Stored in GitHub | Account/service | Rebuilt per device / optional private migration |
| --- | --- | --- | --- |
| Shared `AGENTS.md` instructions and Common hotwords, three custom skills, helpers, templates | Yes, only under `ChatGPT/.codex` plus its scoped ignore file | Skills still need local discovery | Install into the verified local user skill directory and Codex home; preserve the installed Local section; system/plugin/cache content stays excluded |
| `AGENTS.md` Local hotwords | No | Not restored by login | Keep only in this computer's installed AGENTS.md; preserve during updates and omit from every GitHub sync |
| Both Hakase designs, sprite sheets, metadata, and animation previews | Yes, under `pets/hakase-simple` and `pets/hakase-detailed` | Desktop custom pets are local | Install both manifests and sprite sheets into the resolved Codex home; Refresh in Settings > Pets; preserve selection and unrelated pets |
| Existing WorkReport and EnglishMemoryCard Sites | Verified IDs/URLs and workflow references only | Owner-private Sites, registered source and database | Reconnect same account; verify project/address and owner/access. Never export Site data/source into CyberKit |
| Tools/plugins, bundled runtimes, login | No | Availability depends on account/workspace and tool support | Connect/install on the new device; complete real trust/permission prompts; never copy tokens |
| Daily ActivityWatch job | Instructions only, no automation definitions | Inspect local tasks and accessible Scheduled evidence | Default to this computer without another ownership confirmation. Reuse its task/settings, or create once at 20:00 Asia/Singapore; preserve an existing timezone/model/status/notifications. Local jobs need their owning computer on and app running |
| ActivityWatch and its watchers | No | Not provided by Codex login | Install/start locally; detailed browser tracking needs the extension. Do not silently add tracking software or permissions |
| ActivityWatch history, local report drafts | No | No automatic local-history restoration | Start new local capture/drafts. No history transfer or import |
| Manager chat, delegations, registry and monitor memory | No | Use chat/history only if actually exposed to the current account/tools | Verify real thread/host identity. Start fresh local tracking; do not migrate registries, local histories or session databases |

The user's standing preference is to use the current computer for the daily ActivityWatch review. Bare/setup invocation authorizes that default; do not ask which computer should own it or block local creation because other-device listing is unavailable. Reuse a matching local task, including its manual pause; if none exists, create one at 20:00 Asia/Singapore. An explicit choice of another scheduler takes precedence. Leave other computers' jobs unchanged; report an actually observed overlap without claiming the old job stopped. Multiple indistinguishable local candidates are a concrete conflict: report their IDs and preserve them instead of creating another. Do not pause/migrate old tasks incidentally, resume manually paused jobs, adopt another manager's monitor, or infer remote access to another computer's localhost. Preserve unknown fields/settings and verify the saved recurrence, host and destination after any authorized creation/update.

The manager monitor stays ACTIVE while its latest delegated work is running/queued, then pauses after verified outcomes are reported and no executable work remains. Reported user-action waits may also pause it. Preserve its automation ID, registry, history, cursors and deduplication; record why it paused. Actual manager dispatch/follow-up reactivates the same idle-paused monitor and verifies ACTIVE. Unknown/unavailable status alone is not completion, and explicit manual pauses remain binding. A paused monitor cannot detect an executor independently resumed by the user until the manager is invoked to refresh tracked work.

The user's dispatch preference remains `gpt-6.1-sol` with high reasoning and Normal speed. Check destination availability. Current dispatch tools expose model/reasoning but no speed control, so they cannot enforce or verify Normal speed; select it manually in the app when available. Never edit global settings to approximate it.

## Current gaps and completion check

Account access, watcher installation/permissions and actual local schedule conflicts remain real per-device prerequisites. Lack of other-device schedule visibility is not a setup blocker or a reason for another ownership question. No local-history migration is part of this recipe. Check each skill's concise result; setup is partial whenever its required item is pending.

## Ordered test on this computer or a fresh device

This audit does not delete/reset live hooks, tasks, histories or the manager monitor. If the user later resets setup themselves, preserve the local histories on that device and use Scheduled to verify actual task status; removing a local file is not evidence that an account/other-host job stopped.

1. Run the installer at the checkout root and reopen a chat. Expected: `AGENTS.md` and three skills are discoverable, existing Local hotwords and unrelated configuration remain, and a fresh installation contains only shared instructions and Common hotwords. Run again: zero changed instruction/skill files and no duplicate Local section. Before syncing, verify the staged AGENTS.md excludes Local entirely. If the verified scanner uses `.agents/skills`, pass that directory explicitly.
2. Bare-invoke `$activitywatch-life-review`. Expected: current host is discovered in the in-app browser and watcher evidence checked; the local daily task is reused, or created once at 20:00 Asia/Singapore, without asking which computer owns it even when other-device listing is unavailable. Missing installation, extension/permissions or history is reported accurately. Repeat: same task ID, no second schedule; an existing manual pause stays paused. Setup does not produce a habits review or silently install tracking software.
3. In the intended manager chat, bare-invoke `$task-manager`. Expected: that exact chat is renamed/pinned and one matching monitor is reused/created with verified ownership, PAUSED when there is no work. Dispatch actual work: the same automation is ACTIVE while its latest delegated turn is running/queued, then PAUSED after reported outcomes leave nothing executable. Repeat: same monitor ID and preserved registry/cursors/dedupe; a genuinely new chat has fresh local tracking rather than imported records. Explicit manual pauses and other paused jobs stay paused.
4. Bare-invoke `$personal-work-report`. Expected: runtime/template checks, missing Documents `Codex\WorkReports` created, optional hub access status. No report, task or publication. Then request an actual report/review explicitly when desired; it must follow that workflow instead of repeating setup.
5. In Scheduled, verify every actual host/destination, timezone/next run, status and notifications. Keep the scheduler's computer on and app running. An unavailable tool or concrete local conflict leaves that part pending; do not call it rebuilt from file checks alone. Unavailable other-device listing alone does not require confirmation or prevent local daily setup.

These instructions were audited against [Build skills](https://learn.chatgpt.com/docs/build-skills), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), and [Scheduled tasks](https://learn.chatgpt.com/docs/automations). They support file-based customization, explicit skill invocation and local job requirements; they do not establish automatic cross-computer restoration of local state. ActivityWatch prerequisites are documented in its [getting-started guide](https://docs.activitywatch.net/en/latest/getting-started.html) and [watcher guide](https://docs.activitywatch.net/en/latest/watchers.html). Recheck current tools and docs on the target device.
