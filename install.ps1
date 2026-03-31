# claude-config installer — Windows PowerShell wrapper
# Usage: .\install.ps1 [--auto] [--root C:\path]
# Finds Git Bash and runs install.sh through it

$ErrorActionPreference = "Stop"

# Find Git Bash
$gitBashPaths = @(
    "$env:ProgramFiles\Git\bin\bash.exe",
    "$env:ProgramFiles(x86)\Git\bin\bash.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
)

$bashExe = $null
foreach ($p in $gitBashPaths) {
    if (Test-Path $p) { $bashExe = $p; break }
}

if (-not $bashExe) {
    Write-Host "Git Bash bulunamadi. Kur: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

Write-Host "Git Bash: $bashExe" -ForegroundColor Green

# Ensure gh is in PATH
$ghPath = "$env:ProgramFiles\GitHub CLI"
if (Test-Path $ghPath) {
    $env:PATH += ";$ghPath"
}

# Convert script path to Unix format for Git Bash
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$unixPath = ($scriptDir -replace '\\', '/' -replace '^([A-Z]):', '/$1').ToLower()

# Pass arguments through
$extraArgs = $args -join " "

# Run install.sh
& $bashExe -l -c "cd '$unixPath' && bash ./install.sh $extraArgs"
