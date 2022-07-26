# Installation

Get NasirPy up and running in minutes! This guide covers different installation methods depending on your use case.

## 📋 Requirements

- **Python 3.6+** (Python 3.8+ recommended)
- **pip** (Python package installer)

!!! info "Python Version Support"
    NasirPy is designed to work with Python 3.6+ to ensure broad compatibility, but we recommend Python 3.8+ for the best experience with async features.

## 🚀 Quick Installation

### Install from GitHub (Recommended)

The easiest way to install NasirPy is directly from GitHub:

```bash
pip install git+https://github.com/itx-nasir/nasirpy.git
```

This installs the latest stable version with all dependencies.

### Install Specific Version

To install a specific release version:

```bash
pip install git+https://github.com/itx-nasir/nasirpy.git@v0.1.0
```

Replace `v0.1.0` with your desired version tag.

## 🛠️ Development Installation

If you want to contribute to NasirPy or modify the source code:

### 1. Clone the Repository

```bash
git clone https://github.com/itx-nasir/nasirpy.git
cd nasirpy
```

### 2. Install in Development Mode

```bash
pip install -e .
```

The `-e` flag installs the package in "editable" mode, so changes to the source code are immediately reflected.

### 3. Install Development Dependencies (Optional)

For running tests and development tools:

```bash
pip install -e ".[dev]"
```

## 🐍 Virtual Environment (Recommended)

It's always a good practice to use virtual environments:

=== "venv (Built-in)"

    ```bash
    # Create virtual environment
    python -m venv nasirpy-env
    
    # Activate (Windows)
    nasirpy-env\Scripts\activate
    
    # Activate (macOS/Linux)
    source nasirpy-env/bin/activate
    
    # Install NasirPy
    pip install git+https://github.com/itx-nasir/nasirpy.git
    ```

=== "conda"

    ```bash
    # Create conda environment
    conda create -n nasirpy-env python=3.8
    
    # Activate environment
    conda activate nasirpy-env
    
    # Install NasirPy
    pip install git+https://github.com/itx-nasir/nasirpy.git
    ```

=== "pipenv"

    ```bash
    # Create Pipfile and install
    pipenv install git+https://github.com/itx-nasir/nasirpy.git
    
    # Activate shell
    pipenv shell
    ```

## 📦 Dependencies

NasirPy has minimal dependencies to keep it lightweight:

- **uvicorn** - ASGI server for running applications

These are automatically installed when you install NasirPy.

## ✅ Verify Installation

Test that NasirPy is installed correctly:

```python
# test_installation.py
from nasirpy import App, Response

app = App()

@app.get("/")
async def hello():
    return Response({"message": "NasirPy is working!"})

if __name__ == "__main__":
    print("✅ NasirPy installed successfully!")
    print("🚀 Starting test server...")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Run the test:

```bash
python test_installation.py
```

You should see:
```
✅ NasirPy installed successfully!
🚀 Starting test server...
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Visit `http://127.0.0.1:8000` in your browser to see the response!

## 🔧 Troubleshooting

### Common Issues

#### "Module not found" Error

```bash
ModuleNotFoundError: No module named 'nasirpy'
```

**Solution**: Make sure you're in the correct virtual environment and the installation completed successfully:

```bash
pip list | grep nasirpy
```

#### Git Not Found

```bash
error: Microsoft Visual C++ 14.0 is required
```

**Solution**: Install Git if it's not available:

- **Windows**: Download from [git-scm.com](https://git-scm.com/)
- **macOS**: `brew install git` or install Xcode Command Line Tools
- **Linux**: `sudo apt-get install git` (Ubuntu/Debian) or equivalent

#### Permission Errors

```bash
PermissionError: [Errno 13] Permission denied
```

**Solution**: Use `--user` flag or virtual environment:

```bash
pip install --user git+https://github.com/itx-nasir/nasirpy.git
```

### Getting Help

If you encounter issues:

1. **Check the [GitHub Issues](https://github.com/itx-nasir/nasirpy/issues)** for known problems
2. **Create a new issue** with your error message and system details
3. **Join the discussion** in the repository discussions

## 🎯 Next Steps

Now that NasirPy is installed:

1. **[Quick Start Guide](quickstart.md)** - Build your first API in 5 minutes
2. **[View Examples](https://github.com/itx-nasir/nasirpy/tree/master/examples)** - See real applications
3. **[Explore the Code](https://github.com/itx-nasir/nasirpy)** - Understand how it works

---

!!! success "Ready to Go!"
    You're all set! NasirPy is installed and ready for you to start learning web framework internals. 