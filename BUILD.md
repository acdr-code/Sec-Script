# Building and Installing SecScript

To run `.secs` files using the `seclang` CLI, you first need to install SecScript.

### Installation

1. Clone the repository and navigate to its root directory.
2. Install SecScript and its dependencies:

**Windows:**
```powershell
python -m pip install .
```

**Linux / macOS:**
```bash
python3 -m pip install .
```

### Usage

After installation, you can run SecScript from any directory:

```bash
seclang /path/to/project.secs
```

On Windows:

```powershell
seclang C:\path\to\project.secs
```

**Notes:**
- Python must be installed on your system.
- SecScript's dependencies are installed automatically through its package configuration.
- Make sure Python's scripts directory is available in your system's `PATH`.
- A virtual environment is optional, but recommended to avoid dependency conflicts.
