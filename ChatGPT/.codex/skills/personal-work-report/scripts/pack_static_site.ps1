param(
  [Parameter(Mandatory=$true)][string]$SiteRoot,
  [Parameter(Mandatory=$true)][string]$ArchivePath,
  [Parameter(Mandatory=$true)][string]$SitesPluginRoot,
  [Parameter(Mandatory=$true)][string]$NodePath
)
$ErrorActionPreference = 'Stop'
$sitePath = (Resolve-Path -LiteralPath $SiteRoot).Path
$archive = [IO.Path]::GetFullPath($ArchivePath)
$archiveParent = Split-Path -Parent $archive
$stage = Join-Path $archiveParent ('site-package-' + [guid]::NewGuid().ToString('N'))
if (Test-Path -LiteralPath $stage) { throw 'Fresh package staging unexpectedly exists.' }
New-Item -ItemType Directory -Path $stage -Force | Out-Null
$helper = Join-Path $SitesPluginRoot 'skills/sites/scripts/prepare-site-build.cjs'
& $NodePath $helper $sitePath (Join-Path $stage 'dist')
if ($LASTEXITCODE -ne 0) { throw 'Sites static preparation failed.' }
& "$env:WINDIR/System32/tar.exe" -C $stage -czf $archive dist
if ($LASTEXITCODE -ne 0) { throw 'Native archive creation failed.' }
$entries = & "$env:WINDIR/System32/tar.exe" -tzf $archive
if ('dist/.openai/hosting.json' -notin $entries -or 'dist/index.html' -notin $entries) { throw 'Archive lacks the manifest or entrypoint.' }
Write-Output $archive
