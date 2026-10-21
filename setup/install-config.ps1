[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$RepositoryPath,
    [string]$CodexHomePath = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex' }),
    [string]$SkillsPath
)
$ErrorActionPreference = 'Stop'
foreach($path in @($RepositoryPath,$CodexHomePath)) {
    if(-not [IO.Path]::IsPathRooted($path)) { throw 'Repository and Codex home paths must be absolute.' }
}
$source = [IO.Path]::GetFullPath((Join-Path $RepositoryPath 'ChatGPT\.codex'))
$target = [IO.Path]::GetFullPath($CodexHomePath).TrimEnd('\')
if(-not $SkillsPath) { $SkillsPath = Join-Path $target 'skills' }
if(-not [IO.Path]::IsPathRooted($SkillsPath)) { throw 'SkillsPath must be absolute.' }
$skillTarget = [IO.Path]::GetFullPath($SkillsPath).TrimEnd('\')
if($target -eq $source -or $target.StartsWith($source + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Install outside the repository backup subtree.' }
if($skillTarget -eq $source -or $skillTarget.StartsWith($source + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Install skills outside the repository backup subtree.' }
function Destination([string]$Relative) {
    if($Relative.StartsWith('skills\')) { return Join-Path $skillTarget $Relative.Substring(7) }
    return Join-Path $target $Relative
}
function Assert-NoLink([string]$Path) {
    $current = [IO.Path]::GetFullPath($Path)
    while($current) {
        if(Test-Path -LiteralPath $current) {
            if((Get-Item -LiteralPath $current -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked path needs manual review: $current" }
        }
        $parent = Split-Path -Parent $current
        if($parent -eq $current) { break }
        $current = $parent
    }
}
$names = @('activitywatch-life-review','personal-work-report','task-manager')
$files = @([pscustomobject]@{Source=(Join-Path $source 'AGENTS.md');Relative='AGENTS.md'})
foreach($name in $names) {
    $root = Join-Path (Join-Path $source 'skills') $name
    if(-not (Test-Path -LiteralPath (Join-Path $root 'SKILL.md') -PathType Leaf)) { throw "Missing skill: $name" }
    Assert-NoLink $root
    $items = @(Get-ChildItem -LiteralPath $root -Force -Recurse)
    foreach($item in $items) {
        if($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Skill packages must not contain links.' }
        if($item.PSIsContainer) { continue }
        if($item.FullName -match '[\\/](?:__pycache__|node_modules|\.git)[\\/]' -or
           $item.Name -match '^(?:\.env(?:\..*)?|auth\.json|hooks\.json|config\.toml|registry\.json|memory\.md)$' -or
           $item.Extension -in @('.pyc','.pyo','.log','.sqlite','.jsonl','.zip','.gz')) { continue }
        $files += [pscustomobject]@{Source=$item.FullName;Relative=('skills\' + $name + '\' + $item.FullName.Substring($root.Length+1))}
    }
}
foreach($file in $files) {
    Assert-NoLink $file.Source
    if(-not (Test-Path -LiteralPath $file.Source -PathType Leaf)) { throw "Missing source: $($file.Relative)" }
    $destination=Destination $file.Relative
    Assert-NoLink $destination
    if((Test-Path -LiteralPath $destination) -and -not (Test-Path -LiteralPath $destination -PathType Leaf)) { throw "Destination is not a file: $destination" }
    $parent=Split-Path -Parent $destination
    while($parent) {
        if((Test-Path -LiteralPath $parent) -and -not (Test-Path -LiteralPath $parent -PathType Container)) { throw "Destination parent is not a directory: $parent" }
        $next=Split-Path -Parent $parent
        if($next -eq $parent){break}
        $parent=$next
    }
}
$agentsSource = [IO.File]::ReadAllText((Join-Path $source 'AGENTS.md'))
if($agentsSource -match '(?m)^### Local[ \t]*\r?$') { throw 'Repository AGENTS.md must not contain a Local section.' }
$backupRoot = Join-Path $target ('backups\CyberKit\' + [guid]::NewGuid().ToString('N'))
$changed = 0
foreach($file in $files) {
    $destination = Destination $file.Relative
    $sourceHash = (Get-FileHash -LiteralPath $file.Source -Algorithm SHA256).Hash
    $hash = $sourceHash
    $content = $null
    if($file.Relative -eq 'AGENTS.md' -and (Test-Path -LiteralPath $destination -PathType Leaf)) {
        $installed = [IO.File]::ReadAllText($destination)
        $localSections = [regex]::Matches($installed,'(?ms)^### Local[ \t]*\r?\n.*?(?=^#{1,3}[ \t]+|\z)')
        if($localSections.Count -gt 1) { throw 'Installed AGENTS.md has multiple Local sections; reconcile them before updating.' }
        if($localSections.Count -eq 1) {
            $newline = if($installed.Contains("`r`n")) { "`r`n" } else { "`n" }
            $shared = [regex]::Replace($agentsSource,'\r?\n',$newline).TrimEnd()
            $content = [Text.UTF8Encoding]::new($false).GetBytes($shared + $newline + $newline + $localSections[0].Value)
            $hash = [BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($content)).Replace('-','')
        }
    }
    if((Test-Path -LiteralPath $destination -PathType Leaf) -and (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -eq $hash) { continue }
    $null = [IO.Directory]::CreateDirectory((Split-Path -Parent $destination))
    $temporary = $destination + '.install-' + [guid]::NewGuid().ToString('N') + '.tmp'
    if($null -ne $content) { [IO.File]::WriteAllBytes($temporary,$content) }
    else { Copy-Item -LiteralPath $file.Source -Destination $temporary }
    if((Get-FileHash -LiteralPath $temporary -Algorithm SHA256).Hash -ne $hash -or (Get-FileHash -LiteralPath $file.Source -Algorithm SHA256).Hash -ne $sourceHash) { throw 'Source changed during installation; no replacement made for this file.' }
    if(Test-Path -LiteralPath $destination) {
        $backup = Join-Path $backupRoot $file.Relative
        $null = [IO.Directory]::CreateDirectory((Split-Path -Parent $backup))
        [IO.File]::Replace($temporary,$destination,$backup)
    } else { [IO.File]::Move($temporary,$destination) }
    $changed++
}
[pscustomobject]@{codex_home=$target;skills_path=$skillTarget;custom_skills=$names;changed_files=$changed;backup_directory=$(if(Test-Path -LiteralPath $backupRoot){$backupRoot}else{$null});runtime_state_copied=$false;next='Verify this app discovers SkillsPath; reopen a chat and invoke each skill. Existing AGENTS.override.md can take precedence; inspect active instructions without removing it.'} | ConvertTo-Json -Depth 4
