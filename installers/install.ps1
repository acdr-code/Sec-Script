```powershell
$ErrorActionPreference = "Stop"

$VERSION = "1.0.0-pre"
$REPO = "acdr-code/Sec-Script"
$TAG = "v$VERSION"

$TEMP_DIR = Join-Path $env:TEMP ([guid]::NewGuid().ToString())

function Stop-Installer {
    param([string]$Message)

    Write-Host ""
    Write-Host "Installation failed: $Message" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    Write-Host "================================"
    Write-Host "       SecScript Installer"
    Write-Host "================================"
    Write-Host "Version: $VERSION"
    Write-Host ""

    New-Item -ItemType Directory -Path $TEMP_DIR | Out-Null

    # Check winget
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget is required. Install Microsoft App Installer first."
    }

    # Install Python if missing
    $Python = Get-Command py -ErrorAction SilentlyContinue

    if (-not $Python) {
        Write-Host "[1/4] Installing Python..."

        winget install --id Python.Python.3.12 `
            --exact `
            --scope user `
            --silent `
            --accept-package-agreements `
            --accept-source-agreements

        # Refresh PATH
        $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") +
                    ";" +
                    [Environment]::GetEnvironmentVariable("Path", "User")

        $Python = Get-Command py -ErrorAction SilentlyContinue

        if (-not $Python) {
            throw "Python was installed, but the Python launcher is unavailable. Restart PowerShell and run the installer again."
        }
    }

    # Check Python version
    py -3 -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10 or newer is required.'"

    # Install pipx if missing
    Write-Host "[2/4] Preparing pipx..."

    py -3 -m pip install --user pipx

    # Download SecScript
    Write-Host "[3/4] Downloading SecScript..."

    $DOWNLOAD_URL = "https://github.com/$REPO/archive/refs/tags/$TAG.zip"
    $ZIP_PATH = Join-Path $TEMP_DIR "secscript.zip"

    Invoke-WebRequest -Uri $DOWNLOAD_URL -OutFile $ZIP_PATH

    # Extract source
    Expand-Archive -Path $ZIP_PATH -DestinationPath $TEMP_DIR

    $PROJECT_DIR = Join-Path $TEMP_DIR "Sec-Script-$VERSION"

    if (-not (Test-Path (Join-Path $PROJECT_DIR "pyproject.toml"))) {
        throw "Invalid SecScript release archive."
    }

    # Install SecScript
    Write-Host "[4/4] Installing SecScript..."

    py -3 -m pipx install $PROJECT_DIR --force

    # Configure PATH
    py -3 -m pipx ensurepath

    $PIPX_BIN = Join-Path $env:USERPROFILE ".local\bin"
    $env:Path += ";$PIPX_BIN"

    if (-not (Get-Command seclang -ErrorAction SilentlyContinue)) {
        throw "SecScript was installed, but seclang is not available in PATH. Restart PowerShell and try again."
    }

    Write-Host ""
    Write-Host "================================"
    Write-Host "SecScript $VERSION installed!"
    Write-Host "================================" -ForegroundColor Green

    seclang --help
}
catch {
    Stop-Installer $_.Exception.Message
}
finally {
    if (Test-Path $TEMP_DIR) {
        Remove-Item $TEMP_DIR -Recurse -Force
    }
}

Read-Host "Press Enter to exit"
```