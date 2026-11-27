#!/usr/bin/env bash

set -Eeuo pipefail

VERSION="1.0.0-pre"
REPO="acdr-code/Sec-Script"
TAG="v${VERSION}"

TEMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap 'status=$?; echo; echo "Installation failed (exit code: $status)"; read -rp "Press Enter to exit..."' ERR

echo "================================"
echo "       SecScript Installer"
echo "================================"
echo "Version: $VERSION"
echo

# Check sudo
if ! command -v sudo >/dev/null 2>&1; then
    echo "Error: sudo is required."
    exit 1
fi

if ! sudo -v; then
    echo "Error: Administrator privileges are required."
    exit 1
fi

# Detect Linux distribution
if [ ! -f /etc/os-release ]; then
    echo "Error: Cannot detect Linux distribution."
    exit 1
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

        sudo pacman -S --needed \
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
        echo "Error: Unsupported Linux distribution: $ID"
        exit 1
        ;;
esac

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

if [ ! -f "$PROJECT_DIR/pyproject.toml" ]; then
    echo "Error: Invalid SecScript archive."
    exit 1
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
echo "SecScript $VERSION installed!"
echo "================================"
