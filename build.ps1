# WinCloud Build Script
# Builds executable using PyInstaller

$APP_NAME = "WinCloud"
$MAIN_SCRIPT = "wincloud_client\main.py"
$VERSION = "1.0.0"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " WinCloud Build Script v$VERSION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR Python not found!" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "[2/6] Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller --quiet
Write-Host "  OK PyInstaller ready" -ForegroundColor Green

# Clean previous builds
Write-Host "[3/6] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
Get-ChildItem -Filter "*.spec" | Remove-Item -Force
Write-Host "  OK Cleaned" -ForegroundColor Green

# Prepare
Write-Host "[4/6] Preparing build..." -ForegroundColor Yellow
Write-Host "  OK Ready" -ForegroundColor Green

# Build executable
Write-Host "[5/6] Building executable..." -ForegroundColor Yellow
Write-Host "  This may take several minutes..." -ForegroundColor Gray

pyinstaller --name=$APP_NAME --onefile --windowed --clean --noconfirm --hidden-import=PyQt6 --hidden-import=zstandard --hidden-import=cryptography $MAIN_SCRIPT

if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK Build successful!" -ForegroundColor Green
} else {
    Write-Host "  ERROR Build failed!" -ForegroundColor Red
    exit 1
}

# Verify
Write-Host "[6/6] Verifying build..." -ForegroundColor Yellow
$exePath = "dist\$APP_NAME.exe"
if (Test-Path $exePath) {
    $fileSize = (Get-Item $exePath).Length / 1MB
    Write-Host "  OK Executable created" -ForegroundColor Green
    Write-Host "  INFO Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
} else {
    Write-Host "  ERROR Executable not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " Build Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $exePath" -ForegroundColor Cyan
Write-Host ""
