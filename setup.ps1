# PowerShell Setup Script for Deepfake Detection Application
# Run this script to set up the entire project

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deepfake Detection - Setup Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found! Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Set-Location backend

Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Creating .env file..." -ForegroundColor Yellow
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✅ .env file created" -ForegroundColor Green
} else {
    Write-Host "⚠️ .env file already exists" -ForegroundColor Yellow
}

Set-Location ..

# Setup Frontend
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Set-Location frontend

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Set-Location ..

# Create necessary directories
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Creating Directories" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$directories = @(
    "backend\uploads",
    "model\saved_models",
    "model\logs",
    "dataset\train\real",
    "dataset\train\fake",
    "dataset\validation\real",
    "dataset\validation\fake"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created: $dir" -ForegroundColor Green
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📋 Next Steps:`n" -ForegroundColor Yellow

Write-Host "1. Start Backend Server:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\activate" -ForegroundColor Gray
Write-Host "   python app.py`n" -ForegroundColor Gray

Write-Host "2. Start Frontend Server (new terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev`n" -ForegroundColor Gray

Write-Host "3. Open Browser:" -ForegroundColor White
Write-Host "   http://localhost:5173`n" -ForegroundColor Gray

Write-Host "4. (Optional) Train Model:" -ForegroundColor White
Write-Host "   - Add images to dataset/train/real/ and dataset/train/fake/" -ForegroundColor Gray
Write-Host "   - Open model/deepfake_model_training.ipynb in Jupyter" -ForegroundColor Gray
Write-Host "   - Run all cells to train`n" -ForegroundColor Gray

Write-Host "For more info, see README.md or QUICKSTART.md" -ForegroundColor Cyan
Write-Host "`n========================================`n" -ForegroundColor Cyan
