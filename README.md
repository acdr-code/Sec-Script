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
├── AST.py

├── convertTypes.py

├── errorHandler.py

├── ex.secs

├── fileHandel.py

├── Grammar.py

├── interpreter.py

├── LICENSE

├── main.py

├── pathResolver.py

├── README.md

├── requirements.txt

└── SecurityStuff.py

## Roadmap

- [ ] Change `python3 path/to/Sec-Script Repo/main.py path/to/project.secs` to `secScript path/to/project.secs` for running your .secs file
- [ ] Add more built-in functions for cybersecurity
- [ ] Add functions for malware analysis
- [ ] Add functions for digital forensics
- [ ] Make a documentation website

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

source venv\bin\activate
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