[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Skills
)

$ErrorActionPreference = 'Stop'
$RepoDir = $PSScriptRoot
$DryRun = $env:DRY_RUN -eq '1'
$RenamedSkills = @{
    'planner' = @('planning')
    'auditor' = @('project-audit')
}

function Test-CliInstalled {
    param([string[]]$Commands, [string[]]$ConfigDirs)

    foreach ($command in $Commands) {
        if (Get-Command $command -ErrorAction SilentlyContinue) { return $true }
    }
    foreach ($dir in $ConfigDirs) {
        if (Test-DirectoryExists $dir) { return $true }
    }
    return $false
}

function Test-DirectoryExists {
    param([string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    try {
        return (Test-Path -LiteralPath $Path -PathType Container -ErrorAction Stop)
    } catch {
        return $false
    }
}

$targets = [System.Collections.Generic.List[object]]::new()
function Add-SkillTarget {
    param([string]$Label, [string]$Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if ($targets.Path -contains $fullPath) { return }
    $targets.Add([pscustomobject]@{ Label = $Label; Path = $fullPath })
}

function Get-RoamingAppDataDir {
    $appData = [Environment]::GetFolderPath('ApplicationData')
    if ([string]::IsNullOrWhiteSpace($appData)) {
        $appData = $env:APPDATA
    }
    return $appData
}

$agentsDir = Join-Path $HOME '.agents'
$codexDir = Join-Path $HOME '.codex'
$appDataDir = Get-RoamingAppDataDir
$kimiDesktopDaimonDir = if ([string]::IsNullOrWhiteSpace($appDataDir)) {
    $null
} else {
    Join-Path $appDataDir 'kimi-desktop/daimon-share/daimon'
}
if (Test-CliInstalled @('claude') @((Join-Path $HOME '.claude'))) {
    Add-SkillTarget 'Claude' (Join-Path $HOME '.claude/skills')
}
if ((Test-CliInstalled @('codex') @($codexDir)) -and -not (Test-DirectoryExists $agentsDir)) {
    Add-SkillTarget 'Codex' (Join-Path $codexDir 'skills')
}
if (Test-CliInstalled @('cursor') @((Join-Path $HOME '.cursor'))) {
    Add-SkillTarget 'Cursor' (Join-Path $HOME '.cursor/skills')
}
if (Test-CliInstalled @('gemini') @((Join-Path $HOME '.gemini'))) {
    Add-SkillTarget 'Gemini' (Join-Path $HOME '.gemini/skills')
}
if (Test-CliInstalled @('kimi', 'kimi-cli', 'kimi-code') @((Join-Path $HOME '.kimi'), (Join-Path $HOME '.kimi-code'))) {
    Add-SkillTarget 'Kimi' (Join-Path $HOME '.kimi/skills')
}
if (Test-DirectoryExists $kimiDesktopDaimonDir) {
    Add-SkillTarget 'Kimi Desktop' (Join-Path $kimiDesktopDaimonDir 'skills')
}
if (Test-CliInstalled @('opencode') @((Join-Path $HOME '.config/opencode'))) {
    Add-SkillTarget 'OpenCode' (Join-Path $HOME '.config/opencode/skills')
}
if (Test-DirectoryExists $agentsDir) {
    Add-SkillTarget 'Shared agents' (Join-Path $agentsDir 'skills')
}

if ($targets.Count -eq 0) {
    throw 'No installed Windows CLI with a known SKILL.md directory was found.'
}

if ($Skills.Count -eq 1 -and $Skills[0] -eq '--list-targets') {
    foreach ($target in $targets) {
        '{0,-14} {1}' -f $target.Label, $target.Path
    }
    exit 0
}

if (-not $Skills -or $Skills.Count -eq 0) {
    $Skills = @(Get-ChildItem -LiteralPath $RepoDir -Directory | Where-Object {
        Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf
    } | Select-Object -ExpandProperty Name)
}

"Source: $RepoDir"
'Environment: Windows'
'Targets:'
foreach ($target in $targets) {
    "  $($target.Label) -> $($target.Path)"
}
if ($DryRun) { '[DRY-RUN: no writes]' }
''

foreach ($skill in $Skills) {
    $source = Join-Path $RepoDir $skill
    $manifest = Join-Path $source 'SKILL.md'
    if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) {
        "Skip ${skill}: missing $skill/SKILL.md"
        continue
    }

    $versionLine = Select-String -LiteralPath $manifest -Pattern '^version:' | Select-Object -First 1
    $version = if ($versionLine) { ($versionLine.Line -split ':', 2)[1].Trim() } else { '?' }
    "== $skill @ $version =="

    foreach ($target in $targets) {
        $destination = Join-Path $target.Path $skill
        $legacyNames = if ($RenamedSkills.ContainsKey($skill)) {
            @($RenamedSkills[$skill])
        } else {
            @()
        }
        if ($DryRun) {
            foreach ($legacyName in $legacyNames) {
                $legacyDestination = Join-Path $target.Path $legacyName
                if (Test-Path -LiteralPath $legacyDestination -PathType Container) {
                    "  [dry] $($target.Label): remove renamed skill $legacyDestination"
                }
            }
            "  [dry] $($target.Label): overlay $source/* -> $destination"
            continue
        }

        foreach ($legacyName in $legacyNames) {
            $legacyDestination = [System.IO.Path]::GetFullPath((Join-Path $target.Path $legacyName))
            $targetRoot = [System.IO.Path]::GetFullPath($target.Path)
            if (-not $legacyDestination.StartsWith($targetRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Refusing to remove path outside target root: $legacyDestination"
            }
            if (Test-Path -LiteralPath $legacyDestination -PathType Container) {
                Remove-Item -LiteralPath $legacyDestination -Recurse -Force
                "  migrated $($target.Label): removed $legacyName"
            }
        }

        New-Item -ItemType Directory -Path $destination -Force | Out-Null
        Copy-Item -Path (Join-Path $source '*') -Destination $destination -Recurse -Force
        "  ok $($target.Label) -> $destination"
    }
    ''
}

'Done.'
