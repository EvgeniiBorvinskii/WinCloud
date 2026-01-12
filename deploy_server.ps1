# WinCloud Server Deployment Script for Windows
# Automates deployment to 5.249.160.54

param(
    [string]$ServerIP = "5.249.160.54",
    [string]$SSHUser = "root",
    [string]$SSHKeyPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " WinCloud Server Deployment to $ServerIP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if SSH/SCP is available
try {
    $null = Get-Command ssh -ErrorAction Stop
    $null = Get-Command scp -ErrorAction Stop
    Write-Host "[OK] SSH/SCP found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] SSH/SCP not found. Please install OpenSSH client:" -ForegroundColor Red
    Write-Host "  Settings > Apps > Optional Features > Add OpenSSH Client" -ForegroundColor Yellow
    exit 1
}

# Prepare server files
Write-Host ""
Write-Host "[1/4] Preparing server files..." -ForegroundColor Yellow
$serverDir = "wincloud_server"
if (-not (Test-Path $serverDir)) {
    Write-Host "[ERROR] Directory '$serverDir' not found" -ForegroundColor Red
    exit 1
}

# Check required files
$requiredFiles = @("server.py", "deploy.sh", "requirements.txt")
foreach ($file in $requiredFiles) {
    $filePath = Join-Path $serverDir $file
    if (-not (Test-Path $filePath)) {
        Write-Host "[ERROR] Required file missing: $file" -ForegroundColor Red
        exit 1
    }
}
Write-Host "  [OK] All files present" -ForegroundColor Green

# Build SCP command
Write-Host ""
Write-Host "[2/4] Uploading files to server..." -ForegroundColor Yellow
Write-Host "  Target: ${SSHUser}@${ServerIP}:/tmp/" -ForegroundColor Gray

$scpArgs = @("-r", $serverDir, "${SSHUser}@${ServerIP}:/tmp/")
if ($SSHKeyPath) {
    $scpArgs = @("-i", $SSHKeyPath) + $scpArgs
}

try {
    & scp @scpArgs
    Write-Host "  [OK] Files uploaded" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Upload failed: $_" -ForegroundColor Red
    exit 1
}

# Execute deployment on server
Write-Host ""
Write-Host "[3/4] Running deployment script on server..." -ForegroundColor Yellow
Write-Host "  This will:" -ForegroundColor Gray
Write-Host "    - Create /srv/WinCloud directory" -ForegroundColor Gray
Write-Host "    - Install Python dependencies" -ForegroundColor Gray
Write-Host "    - Set up systemd service" -ForegroundColor Gray
Write-Host "    - Configure firewall (port 8443)" -ForegroundColor Gray
Write-Host ""

$deployCommands = @"
cd /tmp/wincloud_server && \
chmod +x deploy.sh && \
sudo ./deploy.sh
"@

$sshArgs = @("${SSHUser}@${ServerIP}", $deployCommands)
if ($SSHKeyPath) {
    $sshArgs = @("-i", $SSHKeyPath) + $sshArgs
}

try {
    & ssh @sshArgs
    Write-Host "  [OK] Deployment completed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Deployment failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "To troubleshoot, connect to server manually:" -ForegroundColor Yellow
    Write-Host "  ssh ${SSHUser}@${ServerIP}" -ForegroundColor White
    Write-Host "  journalctl -u wincloud -n 50" -ForegroundColor White
    exit 1
}

# Verify deployment
Write-Host ""
Write-Host "[4/4] Verifying deployment..." -ForegroundColor Yellow

$healthCheckUrl = "https://${ServerIP}:8443/api/v1/health"
Write-Host "  Checking: $healthCheckUrl" -ForegroundColor Gray

try {
    Start-Sleep -Seconds 3
    $response = Invoke-WebRequest -Uri $healthCheckUrl -UseBasicParsing -SkipCertificateCheck -TimeoutSec 10 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] Server is running" -ForegroundColor Green
    }
} catch {
    Write-Host "  [WARNING] Health check failed (this is normal if SSL cert not configured)" -ForegroundColor Yellow
    Write-Host "  Server may still be running. Verify manually:" -ForegroundColor Yellow
    Write-Host "    ssh ${SSHUser}@${ServerIP} 'systemctl status wincloud'" -ForegroundColor White
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " Deployment Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Server Details:" -ForegroundColor Cyan
Write-Host "  URL:           https://${ServerIP}:8443" -ForegroundColor White
Write-Host "  Health Check:  https://${ServerIP}:8443/api/v1/health" -ForegroundColor White
Write-Host "  Storage:       /srv/WinCloud/storage" -ForegroundColor White
Write-Host "  Logs:          journalctl -u wincloud -f" -ForegroundColor White
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  ssh ${SSHUser}@${ServerIP}" -ForegroundColor White
Write-Host "  systemctl status wincloud" -ForegroundColor White
Write-Host "  systemctl restart wincloud" -ForegroundColor White
Write-Host ""
