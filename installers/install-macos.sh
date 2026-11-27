
#!/usr/bin/env bash

set -Eeuo pipefail

VERSION="1.0.0-pre"
REPO="acdr-code/Sec-Script"
TAG="v${VERSION}"

TEMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

fail() {
    echo
    echo "Installation failed: $1"
    exit 1
}

echo "================================"
echo "       SecScript Installer"
echo "================================"
echo "Version: $VERSION"
echo

# Check operating system
if [[ "$(uname -s)" != "Darwin" ]]; then
    fail "This installer only supports macOS."
fi

# Check architecture
ARCH="$(uname -m)"

case "$ARCH" in
    arm64)
        echo "Architecture: Apple Silicon"
        ;;
    x86_64)
        echo "Architecture: Intel"
        ;;
    *)
        fail "Unsupported architecture: $ARCH"
        ;;
esac

# Check Homebrew
if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew is not installed."
    echo
    echo "Please install Homebrew first:"
    echo "https://brew.sh"
    echo
    fail "Homebrew is required."
fi

echo "[1/4] Checking dependencies..."

# Install Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Installing Python..."
    brew install python
fi

PYTHON="$(command -v python3)"

"$PYTHON" -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10 or newer is required.'"

# Install pipx
if ! command -v pipx >/dev/null 2>&1; then
    echo "Installing pipx..."
    brew install pipx
fi

# Ensure pipx is available
if ! command -v pipx >/dev/null 2>&1; then
    export PATH="$(brew --prefix)/bin:$PATH"
fi

if ! command -v pipx >/dev/null 2>&1; then
    fail "pipx could not be found after installation."
fi

echo "[2/4] Downloading SecScript..."

DOWNLOAD_URL="https://github.com/${REPO}/archive/refs/tags/${TAG}.zip"
ZIP_PATH="$TEMP_DIR/secscript.zip"

if ! curl -fL "$DOWNLOAD_URL" -o "$ZIP_PATH"; then
    fail "Could not download SecScript version $VERSION."
fi

if ! unzip -q "$ZIP_PATH" -d "$TEMP_DIR"; then
    fail "Could not extract SecScript archive."
fi

PROJECT_DIR="$TEMP_DIR/Sec-Script-${VERSION}"

if [[ ! -f "$PROJECT_DIR/pyproject.toml" ]]; then
    fail "Invalid SecScript release archive."
fi

echo "[3/4] Installing SecScript..."

pipx install "$PROJECT_DIR" --force

echo "[4/4] Configuring PATH..."

pipx ensurepath

PIPX_BIN="$(pipx environment --value PIPX_BIN_DIR 2>/dev/null || true)"

if [[ -n "$PIPX_BIN" ]]; then
    export PATH="$PIPX_BIN:$PATH"
fi

# Common Homebrew and pipx locations
export PATH="$(brew --prefix)/bin:$HOME/.local/bin:$PATH"

if ! command -v seclang >/dev/null 2>&1; then
    echo
    echo "SecScript was installed, but seclang is not available in PATH."
    echo "Restart your terminal and try:"
    echo "seclang --help"
    exit 1
fi

echo
echo "================================"
echo "SecScript $VERSION installed!"
echo "================================"

seclang --help
