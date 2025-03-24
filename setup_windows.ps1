# Setup script for Llama 2 Chatbot on Windows
Write-Host "Setting up Llama 2 Chatbot environment..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.10 or higher: https://www.python.org/downloads/" -ForegroundColor Red
    exit
}

# Check if pip is installed
try {
    $pipVersion = pip --version
    Write-Host "✅ Pip detected: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Pip not found. Please ensure pip is installed with Python." -ForegroundColor Red
    exit
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if Ollama is installed
$ollamaInstalled = $false
try {
    $ollamaPath = Get-Command ollama -ErrorAction Stop
    $ollamaInstalled = $true
    Write-Host "✅ Ollama is already installed at: $($ollamaPath.Source)" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama is not installed or not in your PATH." -ForegroundColor Red
}

if (-not $ollamaInstalled) {
    Write-Host "Would you like to download Ollama now? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "Y" -or $response -eq "y") {
        $downloadUrl = "https://ollama.ai/download/windows"
        $installerPath = "$env:TEMP\ollama-installer.exe"
        
        Write-Host "Downloading Ollama installer..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath
        
        Write-Host "Download complete. Please run the installer at: $installerPath" -ForegroundColor Green
        Write-Host "After installation, please restart your computer or logout and login again to update your PATH." -ForegroundColor Yellow
        
        $openInstaller = Read-Host "Would you like to run the installer now? (Y/N)"
        if ($openInstaller -eq "Y" -or $openInstaller -eq "y") {
            Start-Process $installerPath
        }
    } else {
        Write-Host "Please download and install Ollama manually from: https://ollama.ai/download" -ForegroundColor Yellow
    }
}

Write-Host "`nSetup completed. Next steps:" -ForegroundColor Green
Write-Host "1. Ensure Ollama is installed and running" -ForegroundColor Cyan
Write-Host "2. Download the Llama 2 model with: ollama run llama2" -ForegroundColor Cyan
Write-Host "3. Run the direct chatbot interface with: python -m src.modules.llm.streamlit_app" -ForegroundColor Cyan
Write-Host "4. Or run the API server with: python -m src.modules.api.api_server" -ForegroundColor Cyan
Write-Host "5. And the client with: python -m src.modules.client.streamlit_client" -ForegroundColor Cyan 