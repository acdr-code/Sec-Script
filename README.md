# SecScript

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**A scripting language for security-focused tasks.**

SecScript is a Python-based scripting language designed to simplify common security operations and make security-related workflows easier to write and automate.

It brings together functionality for networking, web requests, cryptography, and remote connections in one scripting environment, with the goal of reducing repetitive code and making security tasks more straightforward.

> **Status:** Early development.

## Features

- **Networking:** DNS operations, network scanning, and banner-related functionality.
- **Traffic Analysis:** ARP operations and packet sniffing.
- **Web:** HTTP requests and web indexing.
- **Cryptography:** Hashing utilities.
- **Remote Connections:** SSH client functionality.
- **Certificates:** TLS certificate checking.

SecScript also includes its own grammar, AST builder, interpreter, and error-handling system.

## Installation

SecScript provides installation scripts for Linux, Windows, and macOS. The installers handle the required dependencies and install the `seclang` command.

### Linux

Supported distributions:
- Debian / Ubuntu / Pop!_OS
- Arch Linux / Manjaro
- Fedora

Run:

```bash
curl -fsSL https://raw.githubusercontent.com/acdr-code/Sec-Script/master/installers/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

### Windows

Requires [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/).

Open PowerShell and run:

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/acdr-code/Sec-Script/master/installers/install.ps1" -OutFile "install.ps1"
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

### macOS

Requires [Homebrew](https://brew.sh/) to be installed.

Run:

```bash
curl -fsSL https://raw.githubusercontent.com/acdr-code/Sec-Script/master/installers/install-macos.sh -o install-macos.sh
chmod +x install-macos.sh
./install-macos.sh
```

Supports both Apple Silicon and Intel Macs.

After installation, verify that SecScript is available:

```bash
seclang --help
```

---

## Project Structure

```text
Sec-Script/
├── core/
│   ├── ASTBuild.py
│   ├── ASTNode.py
│   ├── Grammar.py
│   ├── interpreter.py
│   └── errorHandler.py
│
├── fileio/
│
├── installers/
│   ├── install.sh
│   ├── install.ps1
│   └── install-macos.sh
│
├── security/
│   ├── cert/
│   ├── crypto/
│   ├── network/
│   ├── remote/
│   ├── traffic/
│   ├── web/
│   └── SecurityStuff.py
│
├── tests/
│
├── utills/
│
├── main.py
├── pyproject.toml
├── requirements.txt
├── BUILD.md
├── README.md
└── LICENSE
```

## Development

Clone the repository:

```bash
git clone https://github.com/acdr-code/Sec-Script.git
cd Sec-Script
```

Install the project in editable mode:

```bash
pipx install --editable .
```

Changes to the source code will then be reflected without reinstalling the package.

## Roadmap

- [ ] Expand networking capabilities
- [ ] Improve service detection and banner functionality
- [ ] Add malware analysis features
- [ ] Add digital forensics helpers
- [ ] Build a proper documentation website

## License

SecScript is licensed under the [Apache License 2.0](LICENSE).