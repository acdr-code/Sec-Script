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

# Check sudo
if ! command -v sudo >/dev/null 2>&1; then
    fail "sudo is required."
fi

if ! sudo -v; then
    fail "Administrator privileges are required."
fi

# Detect Linux distribution
if [[ ! -f /etc/os-release ]]; then
    fail "Cannot detect Linux distribution."
fi

source /etc/os-release

echo "Detected system: $PRETTY_NAME"
echo

# Install dependencies
case "$ID" in

    ubuntu|debian|pop)
        echo "Using APT..."

        sudo apt-get update || {
            echo "Warning: Some repositories failed to update."
            echo "Continuing with available package lists..."
        }

        sudo apt-get install -y \
            curl \
            unzip \
            python3 \
            python3-venv \
            pipx
        ;;

    arch|manjaro)
        echo "Using Pacman..."

        sudo pacman -S --needed --noconfirm \
            curl \
            unzip \
            python \
            python-pipx
        ;;

    fedora)
        echo "Using DNF..."

        sudo dnf install -y \
            curl \
            unzip \
            python3 \
            pipx
        ;;

    *)
        fail "Unsupported Linux distribution: $ID"
        ;;
esac

# Check Python version
python3 -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10 or newer is required.'"

# Download SecScript
DOWNLOAD_URL="https://github.com/$REPO/archive/refs/tags/$TAG.zip"

echo
echo "[1/3] Downloading SecScript..."

curl -fL "$DOWNLOAD_URL" -o "$TEMP_DIR/secscript.zip"

# Extract source
echo
echo "[2/3] Extracting files..."

unzip -q "$TEMP_DIR/secscript.zip" -d "$TEMP_DIR"

PROJECT_DIR="$TEMP_DIR/Sec-Script-${TAG#v}"

if [[ ! -f "$PROJECT_DIR/pyproject.toml" ]]; then
    fail "Invalid SecScript archive."
fi

# Install SecScript
echo
echo "[3/3] Installing SecScript..."

pipx install "$PROJECT_DIR" --force

# Configure PATH
pipx ensurepath

export PATH="$HOME/.local/bin:$PATH"

# Verify installation
if ! command -v seclang >/dev/null 2>&1; then
    echo
    echo "Installation completed, but seclang is not in PATH."
    echo "Restart your terminal and try again."
    exit 1
fi

echo
echo "================================"
echo "SecScript installed!"
echo "================================"

seclang --help
