# Jarvis Windows PC deployment

Write-Host "=== JARVIS PC SERVICE DEPLOYMENT ===" -ForegroundColor Green
Write-Host ""

# 1. Python setup
Write-Host "[1/4] Python & Dependencies" -ForegroundColor Cyan
Write-Host "Installing via uv..."
pip install uv --quiet
uv sync
Write-Host "OK`n"

# 2. API keys
Write-Host "[2/4] Storing API Keys" -ForegroundColor Cyan
python scripts/setup_keys.py
Write-Host "OK`n"

# 3. Install service
Write-Host "[3/4] Installing Windows Service" -ForegroundColor Cyan
python hands/scripts/install_service.py
Write-Host "OK`n"

# 4. Start service
Write-Host "[4/4] Starting Service" -ForegroundColor Cyan
net start JarvisHands
Start-Sleep -Seconds 2

# Verify
$health = curl -Uri "http://127.0.0.1:8787/health" -UseBasicParsing -ErrorAction SilentlyContinue
if ($health.StatusCode -eq 200) {
    Write-Host "OK - Service healthy`n" -ForegroundColor Green
} else {
    Write-Host "Warning: Service may need restart`n" -ForegroundColor Yellow
}

Write-Host "Deployment complete. Next steps:"
Write-Host "1. UI available at http://127.0.0.1:8787/ui"
Write-Host "2. Enable microphone when prompted"
Write-Host "3. Say 'Hey Jarvis' to activate"
Write-Host "4. Monitor logs in C:\Jarvis\logs\"
