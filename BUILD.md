# Installing SecScript

SecScript provides a command-line interface (CLI) that allows you to execute `.secs` files from any directory.

## Prerequisites

- Python 3.10 or newer
- pipx

### 1. Install Python

If Python is not already installed, download it from [python.org](https://www.python.org/downloads/).

On Windows, make sure to enable **Add Python to PATH** during installation.

### 2. Install pipx

Choose the instructions for your operating system.

**Linux (Debian / Ubuntu):**

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

**macOS:**

```bash
brew install pipx
pipx ensurepath
```

**Windows:**

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

Restart your terminal after installation so the PATH changes take effect.

## Installation

Clone the repository and navigate to its root directory:

```bash
git clone <repository-url>
cd SecScript
```

Install SecScript using pipx:

```bash
pipx install .
```

This installs SecScript and its dependencies in an isolated Python environment.

### Development installation

If you want to work on SecScript's source code, use:

```bash
pipx install --editable .
```

Editable installation allows source code changes to take effect without reinstalling the package.

## Usage

After installation, you can execute `.secs` files from any directory:

```bash
seclang /path/to/project.secs
```

**Windows example:**

```powershell
seclang C:\path\to\project.secs
```

**Linux / macOS example:**

```bash
seclang /path/to/project.secs
```

## Uninstallation

To uninstall SecScript:

```bash
pipx uninstall secscript
```

## Notes

- Python 3.10 or newer is required.
- Dependencies are installed automatically through `pyproject.toml`.
- pipx keeps SecScript's dependencies isolated from your system Python.
- Make sure pipx's executable directory is available in your system's PATH.
- A virtual environment is not required for using the installed CLI.
