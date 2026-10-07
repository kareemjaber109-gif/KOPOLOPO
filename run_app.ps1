$PROJECT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_DIR

# ===== Ensure writable config folder inside the project =====
$HOME_DIR = Join-Path $PROJECT_DIR "_userhome"
$CFG_DIR  = Join-Path $PROJECT_DIR ".streamlit"
New-Item -ItemType Directory -Path $HOME_DIR -Force | Out-Null
New-Item -ItemType Directory -Path $CFG_DIR  -Force | Out-Null

# ===== Force Streamlit + user folders into the project (no permission errors) =====
$env:HOME                = $HOME_DIR
$env:USERPROFILE         = $HOME_DIR
$env:STREAMLIT_CONFIG_DIR= $CFG_DIR
$env:STREAMLIT_BROWSER_GATHER_USAGE_STATS = "false"

Write-Host "Project dir : $PROJECT_DIR"
Write-Host "HOME        : $env:HOME"
Write-Host "Config dir  : $env:STREAMLIT_CONFIG_DIR"
Write-Host "Starting Streamlit dashboard..."
Write-Host ""

& streamlit run app.py --server.headless true --server.port 8501 --server.address 127.0.0.1 --browser.gatherUsageStats false
