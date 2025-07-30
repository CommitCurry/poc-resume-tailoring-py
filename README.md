# CommitCurry

A command line application for CommitCurry.

## Prerequisites

**Python Version:** Requires Python 3.8 or higher (Python 3.13+ recommended)

**Environment Management Tools:**
- **pyenv** - For Python version management
- **uv** - Modern Python package manager (recommended)

### Installing Prerequisites (macOS)

```bash
# Install pyenv and uv via Homebrew
brew install pyenv pyenv-virtualenv uv

# Add pyenv to your shell configuration
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

# Reload shell configuration
source ~/.zshrc
```

### Verify Your Environment

```bash
# Check Python version (should be 3.8+)
python3 --version

# Check if uv is installed
uv --version

# Check if pyenv is working
pyenv --version
```

## Installation

### Recommended Method (using uv)

```bash
# Create virtual environment
uv venv .venv --python 3.13

# Activate virtual environment
source .venv/bin/activate

# Install project with development dependencies
uv pip install -e ".[dev]"
```

### Alternative Method (using pip)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project with development dependencies
pip install -e ".[dev]"
```

## Usage

**Make sure your virtual environment is activated first:**
```bash
source .venv/bin/activate
```

**Run the application:**
```bash
commitcurry
```

**Alternative methods:**
```bash
# Via Python module
python -m commitcurry.main

# Direct path (if in PATH)
/path/to/.venv/bin/commitcurry
```

## Development

**Always activate your virtual environment first:**
```bash
source .venv/bin/activate
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v

# Run tests without coverage
pytest --no-cov
```

### Code Quality

```bash
# Lint code
ruff check .

# Format code
ruff format .

# Auto-fix linting issues
ruff check --fix .

# Type checking
mypy src/
```

### Environment Management

```bash
# Create new virtual environment
uv venv .venv --python 3.13

# Activate virtual environment
source .venv/bin/activate

# Deactivate virtual environment
deactivate

# List installed packages
uv pip list

# Install new package
uv pip install <package-name>

# Install from requirements
uv pip install -r requirements.txt
```

### Development Workflow

1. **Setup (one time):**
   ```bash
   uv venv .venv --python 3.13
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

2. **Daily development:**
   ```bash
   source .venv/bin/activate  # Always do this first
   # Make your changes...
   pytest                     # Run tests
   ruff check --fix .         # Lint and fix
   ruff format .              # Format code
   mypy src/                  # Type check
   ```

3. **Before committing:**
   ```bash
   source .venv/bin/activate
   pytest                     # Ensure tests pass
   ruff check .               # Ensure no lint errors
   mypy src/                  # Ensure no type errors
   ```