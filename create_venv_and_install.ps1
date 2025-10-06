<#
.SYNOPSIS
  Creates a Python virtual environment and installs packages from patient-api/requirements.txt (PowerShell)

.NOTES
  Run this script from the project root. If execution is restricted, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#>

param(
  [string]$RequirementsPath = "patient-api/requirements.txt",
  [string]$VenvDir = "venv"
)

function Find-Python {
  $py = Get-Command python -ErrorAction SilentlyContinue
  if ($py) { return "python" }
  $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
  if ($pyLauncher) { return "py -3" }
  return $null
}

$pythonExe = Find-Python
if (-not $pythonExe) {
  Write-Error "Python not found. Install Python 3 and ensure 'python' or 'py' is on PATH." -ErrorAction Stop
}

if (-not (Test-Path -Path $VenvDir)) {
  & $pythonExe -m venv $VenvDir
  if ($LASTEXITCODE -ne 0) { Write-Error "Failed to create virtual environment." -ErrorAction Stop }
} else {
  Write-Output "Using existing virtual environment: $VenvDir"
}

Write-Output "Activating venv..."
.
Join-Path (Get-Location) $VenvDir | Out-Null
$activate = Join-Path $VenvDir 'Scripts\Activate.ps1'
if (Test-Path $activate) { . $activate } else { Write-Warning "Activate script not found. You can activate manually: .\$VenvDir\Scripts\Activate.ps1" }

Write-Output "Upgrading pip and installing requirements from $RequirementsPath"
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r $RequirementsPath

Write-Output "Done. To activate the venv later in PowerShell run: .\$VenvDir\Scripts\Activate.ps1"
