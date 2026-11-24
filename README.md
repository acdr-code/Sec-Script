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

SecScript can be installed using `pipx`, which keeps its dependencies isolated from your system Python environment.

See [BUILD.md](BUILD.md) for installation instructions on Linux, macOS, and Windows.

## Usage

After installation, run a SecScript file using:

```bash
seclang path/to/file.secs
```

For example:

```bash
seclang tests/ex.secs
```

You can also use an absolute path:

```bash
seclang /path/to/project.secs
```

## Project Structure

```text
SecScript/
├── core/
│   ├── __init__.py
│   ├── ASTBuild.py
│   ├── ASTNode.py
│   ├── errorHandler.py
│   ├── Grammar.py
│   └── interpreter.py
│
├── fileio/
│   ├── __init__.py
│   ├── fileHandel.py
│   └── pathResolver.py
│
├── security/
│   ├── cert/
│   │   ├── __init__.py
│   │   └── tsl.py
│   ├── crypto/
│   │   ├── __init__.py
│   │   └── hash.py
│   ├── network/
│   │   ├── __init__.py
│   │   ├── banner.py
│   │   ├── dns.py
│   │   └── scanning.py
│   ├── remote/
│   │   ├── __init__.py
│   │   └── sshclient.py
│   ├── traffic/
│   │   ├── __init__.py
│   │   ├── arp.py
│   │   └── sniffing.py
│   ├── web/
│   │   ├── __init__.py
│   │   ├── indexing.py
│   │   └── requests.py
│   └── SecurityStuff.py
│
├── utills/
│   ├── __init__.py
│   └── convertTypes.py
│
├── tests/
│   ├── asdasd.secs
│   └── ex.secs
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

### Version 0.1.0

- [x] Basic language features (variables, loops, functions, ...)
- [x] SSH, HTTP, DNS, hashing, and TLS checking
- [x] ARP scanning
- [x] Improved CLI (`seclang` command)

### Future

- [ ] Expand networking capabilities
- [ ] Improve service detection and banner functionality
- [ ] Add malware analysis features
- [ ] Add digital forensics helpers
- [ ] Build a proper documentation website
- [ ] Provide a standalone installer

## License

SecScript is licensed under the [Apache License 2.0](LICENSE).