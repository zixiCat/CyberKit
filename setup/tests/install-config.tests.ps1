# Isolated regression checks; never reads or writes the user's Codex home.
$ErrorActionPreference = 'Stop'
$repository = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$installer = Join-Path $repository 'setup\install-config.ps1'
$template = [IO.File]::ReadAllText((Join-Path $repository 'setup\templates\agents-local.example.md'))
$fixture = Join-Path ([IO.Path]::GetTempPath()) ('cyberkit-install-test-' + [guid]::NewGuid().ToString('N'))
$fixture = [IO.Path]::GetFullPath($fixture)
$utf8 = [Text.UTF8Encoding]::new($false)
$checks = 0
function Assert([bool]$Condition, [string]$Message) {
    if(-not $Condition) { throw $Message }
    $script:checks++
}
function Write-Fixture([string]$Path, [string]$Content) {
    $null = [IO.Directory]::CreateDirectory((Split-Path -Parent $Path))
    [IO.File]::WriteAllText($Path, $Content, $utf8)
}
function Install([string]$HomePath, [switch]$PetsOnly) {
    & $installer -RepositoryPath $source -CodexHomePath $HomePath -SkillsPath $skillPath -PetsOnly:$PetsOnly | ConvertFrom-Json
}
function Expect-Failure([scriptblock]$Action, [string]$Pattern) {
    $failure = $null
    try { & $Action | Out-Null } catch { $failure = $_.Exception.Message }
    Assert ($null -ne $failure -and $failure -match $Pattern) "Expected failure matching: $Pattern"
}
try {
    $source = Join-Path $fixture 'repository'
    $skillPath = Join-Path $fixture 'custom-skills'
    $agentsSource = Join-Path $source 'ChatGPT\.codex\AGENTS.md'
    $shared = "### Common`n`n- SharedFixture`n"
    Write-Fixture $agentsSource $shared
    Write-Fixture (Join-Path $source 'setup\templates\agents-local.example.md') $template
    foreach($name in @('activitywatch-life-review','personal-work-report','hakase','eruna')) {
        Write-Fixture (Join-Path $source "ChatGPT\.codex\skills\$name\SKILL.md") "# Synthetic $name"
    }
    foreach($name in @('hakase-simple','hakase-detailed')) {
        Write-Fixture (Join-Path $source "pets\$name\pet.json") '{}'
        Write-Fixture (Join-Path $source "pets\$name\spritesheet.png") 'synthetic asset'
    }
    Write-Fixture (Join-Path $skillPath 'unrelated\SKILL.md') 'untouched skill'
    $fresh = Join-Path $fixture 'fresh-home'
    $agents = Join-Path $fresh 'AGENTS.md'
    $sentinels = @('config.toml','eruna\queue.sqlite','history.jsonl','pets\selection.json','schedules\local.json','project-instructions\private.md')
    foreach($relative in $sentinels) { Write-Fixture (Join-Path $fresh $relative) "untouched $relative" }
    $first = Install $fresh
    $expected = $shared.TrimEnd() + "`n`n" + [regex]::Replace($template,'\r?\n',"`n")
    Assert ([IO.File]::ReadAllText($agents) -ceq $expected) 'Fresh install must append exactly the generic template.'
    Assert ($first.skills_path -eq $skillPath) 'Explicit skills directory must be respected.'
    Assert ((Install $fresh).changed_files -eq 0) 'Repeated fresh install must make zero changes.'
    foreach($relative in $sentinels) {
        Assert ([IO.File]::ReadAllText((Join-Path $fresh $relative)) -ceq "untouched $relative") "Unrelated file changed: $relative"
    }
    Assert ([IO.File]::ReadAllText((Join-Path $skillPath 'unrelated\SKILL.md')) -ceq 'untouched skill') 'Unrelated skill changed.'

    Write-Fixture $agents $shared
    $upgrade = Install $fresh
    Assert ([IO.File]::ReadAllText($agents) -ceq $expected) 'Update missing Local must append the template.'
    Assert ([IO.File]::ReadAllText((Join-Path $upgrade.backup_directory 'AGENTS.md')) -ceq $shared) 'Original instructions must be backed up.'
    Assert ((Install $fresh).changed_files -eq 0) 'Repeated upgrade must make zero changes.'

    foreach($newline in @("`n", "`r`n")) {
        foreach($ending in @('', $newline)) {
            $local = '### Local  ' + $newline + $newline + '- PrivateFixture-' + [char]0xE9 + $newline + '#### Private project instructions' + $newline + '- Synthetic private mapping  ' + $ending
            Write-Fixture $agents ("### Common`n- OldShared`n`n" + $local)
            $update = Install $fresh
            $actual = [IO.File]::ReadAllText($agents)
            $match = [regex]::Match($actual,'(?ms)^### Local[ \t]*(?:\r?\n|\z).*?(?=^#{1,3}[ \t]+|\z)')
            Assert ($match.Value -ceq $local) 'Private Local content, whitespace, Unicode and line endings must survive verbatim.'
            Assert ($actual.Contains('SharedFixture') -and -not $actual.Contains('OldShared')) 'Shared instructions must still update.'
            Assert ((Install $fresh).changed_files -eq 0) 'Repeated private Local update must make zero changes.'
        }
    }
    Write-Fixture $agents ($shared + "`n### Local")
    $null = Install $fresh
    Assert ([IO.File]::ReadAllText($agents).EndsWith('### Local')) 'Empty Local heading without a trailing newline must be preserved.'
    Assert ((Install $fresh).changed_files -eq 0) 'Empty Local heading must remain idempotent.'

    $duplicate = $shared + "`n### Local`n- First`n### Local"
    Write-Fixture $agents $duplicate
    Expect-Failure { Install $fresh } 'multiple Local sections'
    Assert ([IO.File]::ReadAllText($agents) -ceq $duplicate) 'Duplicate rejection must leave installed instructions unchanged.'
    Write-Fixture $agentsSource ($shared + "`n### Local`n- Forbidden")
    Expect-Failure { Install $fresh } 'Repository AGENTS.md must not contain a Local section'
    Write-Fixture $agentsSource $shared
    Assert (-not [IO.File]::ReadAllText($agentsSource).Contains('PrivateFixture')) 'Private content must never flow into the source.'

    # Pet-only installation must work without any instruction source/template.
    Remove-Item -LiteralPath $agentsSource
    Remove-Item -LiteralPath (Join-Path $source 'setup\templates\agents-local.example.md')
    $petHome = Join-Path $fixture 'pets-only-home'
    $null = Install $petHome -PetsOnly
    Assert (-not (Test-Path -LiteralPath (Join-Path $petHome 'AGENTS.md'))) 'Pet-only install must not create instructions.'
    Write-Output "PASS: $checks installer checks (fresh, missing Local, private preservation, repeat updates, rejection and pet-only)."
} finally {
    $temporaryRoot = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\')
    if((Split-Path -Parent $fixture) -ne $temporaryRoot -or (Split-Path -Leaf $fixture) -notmatch '^cyberkit-install-test-[0-9a-f]{32}$') {
        throw 'Refusing cleanup outside the isolated temporary fixture.'
    }
    if(Test-Path -LiteralPath $fixture) { Remove-Item -LiteralPath $fixture -Recurse -Force }
}
