# Private project instructions on each computer

CyberKit carries this recipe and a [generic starter template](templates/project-instructions.example.md). Each computer creates its own private project files and folder mappings. Neither the private files nor their mappings belong in CyberKit.

## New-computer checklist

1. Resolve this computer's `CODEX_HOME` (the environment variable, or the current user's `.codex` directory). Use the [normal setup guide](new-computer.md) if shared instructions and skills are not installed yet.
2. Verify the actual absolute root of the project on this computer. Do not reuse a path or project mapping from another device.
3. Create `<resolved CODEX_HOME>/project-instructions/` outside the CyberKit checkout. Create a private `<project-key>.md` only if it does not already exist; start from the generic template and fill it in locally. Preserve an existing file.
4. Add one conditional reference under `### Local` in this computer's installed `AGENTS.md`, as shown below. Preserve its existing hotwords and mappings; do not append a duplicate mapping.
5. Open a new chat in the project and run the matching/nonmatching checks below. Reconcile an existing `AGENTS.override.md` deliberately if it takes precedence; do not delete it during setup.

Copy this task into Codex on the target computer:

```text
Set up computer-local project instructions using https://github.com/zixiCat/CyberKit/blob/main/setup/local-project-instructions.md.

Resolve this computer's Codex home and verify the project root I want to configure; ask for that root if it is not known. Create the project-instructions directory outside the checkout and a private file from the generic template only when missing. Keep any existing private content, Local hotwords and mappings. Add or reconcile only this project's conditional reference inside the installed AGENTS.md Local section, using this computer's verified absolute paths. Keep Local subheadings at level four or deeper. Do not invent private rules or copy another device's Local section, paths or private files.

Verify the rule matches the project root and its descendants, excludes sibling folders, and safely skips a missing private file. Keep private content and mappings off GitHub. Do not run the full installer merely to add this mapping, create worktrees, install pets, change schedules, or publish anything.
```

## Layout and ownership

```text
CyberKit checkout/
  ChatGPT/.codex/AGENTS.md                 shared instructions and Common only
  setup/local-project-instructions.md     this portable recipe
  setup/templates/project-instructions.example.md

<resolved CODEX_HOME>/                     outside the checkout
  AGENTS.md                               shared content + this computer's Local
  project-instructions/
    <project-key>.md                       private rules written on this computer
```

Use repository `AGENTS.md` files for rules that should travel with a project. This separate private directory is for rules or locations that should stay on one computer. Keep credentials out of instruction files entirely.

Codex automatically discovers global and repository `AGENTS.md` files as described in the [official instruction-discovery guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md). It does not automatically discover this arbitrary `project-instructions` directory. The conditional reference in the installed Local section tells the agent when to read a private file; it is an instruction, not a new Codex configuration option or a security boundary.

## Create a starter without replacing an existing file

From the CyberKit checkout root in PowerShell, after choosing a project key for this computer:

```powershell
$projectKey = 'my-project' # Replace with a simple filename key for your project.
if ($projectKey -cnotmatch '^[a-z0-9][a-z0-9-]*$') {
    throw 'Use a lowercase filename key containing only letters, digits and hyphens.'
}
$projectCodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else {
    Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
}
if (-not [IO.Path]::IsPathRooted($projectCodexHome)) {
    throw 'Resolve CODEX_HOME to an absolute path first.'
}
$projectCodexHome = [IO.Path]::GetFullPath($projectCodexHome).TrimEnd('\')
$projectCheckoutRoot = (Get-Location).Path.TrimEnd('\')
if ($projectCodexHome.Equals($projectCheckoutRoot, [StringComparison]::OrdinalIgnoreCase) -or
    $projectCodexHome.StartsWith($projectCheckoutRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Keep the private Codex home outside the checkout.'
}
$privateDirectory = Join-Path $projectCodexHome 'project-instructions'
$privateFile = Join-Path $privateDirectory ($projectKey + '.md')
$starter = Join-Path (Get-Location).Path 'setup/templates/project-instructions.example.md'
$null = [IO.Directory]::CreateDirectory($privateDirectory)
if (-not (Test-Path -LiteralPath $privateFile)) {
    [IO.File]::Copy($starter, $privateFile, $false) # Refuses to overwrite.
}
```

Fill the starter locally before enabling its reference. The snippet creates a file only; it does not edit `AGENTS.md` or infer the project root. Keep the private directory outside any checkout that could be committed or synced.

## Shared content and a private conditional reference

The tracked `ChatGPT/.codex/AGENTS.md` remains the shared source: shared instructions and `### Common` hotwords only. Do not add project paths, private file contents or a Local section to that tracked file.

The following is a **template for the installed file on the target computer only**. Replace every angle-bracket placeholder with that computer's values and merge it into an existing Local section rather than creating a second one:

```markdown
### Local

- <THIS COMPUTER'S LOCAL HOTWORDS>

#### Private project instructions

- Only when the current working directory resolves to `<ABSOLUTE PROJECT ROOT ON THIS COMPUTER>` or a directory beneath it, read `<ABSOLUTE PRIVATE INSTRUCTION FILE ON THIS COMPUTER>` if it exists and apply it alongside the repository instructions. Match the whole project root or a descendant separated by a path separator, never a sibling with a similar name. If the file is missing, skip it and continue with shared and repository instructions. Do not load this file for other projects. Keep this reference and the private file on this computer; never copy them into CyberKit or upload them to GitHub.
```

For the private instruction file, use the resolved path to `project-instructions/<project-key>.md` created above. Repeat the conditional bullet for each project, with its own verified root and private file.

Resolve the project root and working directory using the target computer's path rules before comparing them. On Windows, compare without case sensitivity. Match equality, or a prefix consisting of the **whole root plus a path separator**. A plain text prefix can accidentally match a sibling such as `<PROJECT_ROOT>-archive`; that sibling must not load the private rules. Resolve aliases or links before deciding whether a directory is beneath the root.

Keep all subheadings inside Local at `####` or deeper. The current installer preserves Local through the next heading of level three or higher, or end of file; a new `###` heading ends that private section.

## Updates and verification

The existing `setup/install-config.ps1` updates shared instructions while preserving the target computer's Local section. It does not copy or modify `project-instructions/`. Fresh installations receive no other computer's Local section or mappings. Repeat setup must keep existing private files, reuse the existing Local section, and avoid duplicate project references. Do not run the full installer just to create a private mapping; it also installs skills and pets.

When syncing installed instructions back to CyberKit, omit the entire Local section and its references. Review the staged diff: only shared instructions and Common hotwords belong in the tracked `AGENTS.md`. Keep the actual private files outside the checkout; the ignore rules under `ChatGPT/.codex` are an extra guard, not permission to copy private data there.

Use a harmless marker in a synthetic private file to test the rule without exposing real project instructions:

| Working directory / file state | Expected result |
| --- | --- |
| Exactly `<PROJECT_ROOT>` | Read that project's private file if present. |
| `<PROJECT_ROOT><separator>src` | Read the same private file if present. |
| `<PROJECT_ROOT>-archive` or `<PROJECT_ROOT>-other` | Do not read it. |
| Another project or a parent of `<PROJECT_ROOT>` | Do not read it. |
| Matching directory, private file missing | Skip the file; continue with shared and repository guidance. Do not substitute another project's file or create private rules automatically. |
| Repeat setup/update | Existing Local content and private files remain; no duplicate mappings. |

In a new chat in each test directory, ask which private file applies and to load only a matching existing file. Check the result without printing private contents into reports. File/path checks establish setup correctness; verify actual instruction loading in a new chat as well.
