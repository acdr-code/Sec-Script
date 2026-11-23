# Sec-Script Language

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

A scripting language made for security work (pentest, building security tools, and malware analysis later). Built with pure Python.

## Features

- Made specifically for security tasks. Things that take a lot of code in normal languages are much shorter here.
- Focus on the result, skip the boring parts. Makes it easier to chain tools and build your own security automations.
- Open source and written in pure Python
- Built-in support for common security stuff (SSH, HTTP, DNS, hashing, TLS checking, ...)

## Requirements

- Python 3
- pip
- Libraries listed in `requirements.txt`

## Usage

- Made for cybersecurity work
- Encode, decode and hash with one line
- Common tasks like SSH, HTTP requests and DNS lookups
- TLS certificate checking
- Malware analysis (coming later)

You can see examples in the `ex.secs` file.

## Project Structure
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
├── README.md
└── LICENSE

## Roadmap

### Version 0.x (Current)
- [x] Basic language features (variables, loops, functions, ...)
- [x] SSH, HTTP, DNS, Hashing, TLS check
- [x] ARP Scan (Network Discovery)
- [x] Better CLI (`secs` command instead of `python main.py`)

### Future
- [ ] More network tools (port service detection, banner grabbing, ...)
- [ ] Malware analysis features
- [ ] Digital forensics helpers
- [ ] Proper documentation website
- [ ] Standalone installer (no need for pip/python knowledge)

## Installation

1. Make sure to have [Python](https://www.python.org/) installed on your device
2. Download the project using:
```
git clone https://github.com/acdr-code/Sec-Script.git
```
3. Go to project directory in Terminal
4. Make venv using:
```
python3 -m venv venv
```
5. Activate venv:
```
#on windows

venv\Scripts\activate
```
```
#on linux/macOS

source venv/bin/activate
```
6. Install requirements with:
```
pip install -r requirements.txt
```
7. Run your .secs file with:
```
python3 main.py path/to/project.secs
```

## License

Apache License 2.0
