# ----------------------------
# run_all.ps1
# ----------------------------

# Exit immediately if any command fails
$ErrorActionPreference = "Stop"

Write-Host "========== Starting Environment Setup =========="

# 1️⃣ Activate Python virtual environment
$venvPath = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    . $venvPath
} else {
    Write-Host "No virtual environment found. Creating one..."
    python -m venv .venv
    . $venvPath
}

# 2️⃣ Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "========== Training Models =========="

# 3️⃣ Train Rain Model
Write-Host "Training rain model..."
python models/prediction-of-rainfall.py

# 4️⃣ Train Crop Yield Model
Write-Host "Training crop yield model..."
python models/prediction-of-yield.py

# 5️⃣ Train Fertilizer Model
Write-Host "Training fertilizer model..."
python models/fertilizer-suggestion.py

Write-Host "========== Starting Backend (FastAPI) =========="

# Start FastAPI in background
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
Write-Host "Backend started..."

Write-Host "========== Starting Frontend (Next.js) =========="

# Navigate to frontend folder
Set-Location -Path "frontend"

# Install frontend dependencies if not installed
if (!(Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..."
    npm install
}

# Start Next.js app in development mode (foreground)
Write-Host "Starting Next.js frontend..."
npm run dev
