# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Management

**Python Version Management:**
- **pyenv**: Manages Python versions (installed via Homebrew)
- **uv**: Fast Python package manager and virtual environment tool

**Setup:**
```bash
# Create virtual environment
uv venv .venv --python 3.13

# Activate virtual environment
source .venv/bin/activate

# Install project with dev dependencies
uv pip install -e ".[dev]"
```

## Development Commands

**Installation (legacy method):**
```bash
pip install -e ".[dev]"
```

**Running the application:**
```bash
commitcurry                    # If installed binaries are in PATH
python -m commitcurry.main     # Alternative method
```

**Testing:**
```bash
pytest                         # Run all tests with coverage
pytest tests/test_main.py      # Run specific test file
pytest -v                      # Verbose output
```

**Code Quality:**
```bash
ruff check .                   # Lint code
ruff format .                  # Format code
ruff check --fix .             # Auto-fix linting issues
mypy src/                      # Type checking
```

**Environment Commands:**
```bash
uv venv .venv                  # Create new virtual environment
source .venv/bin/activate      # Activate virtual environment
deactivate                     # Deactivate virtual environment
uv pip list                    # List installed packages
uv pip install <package>       # Install new package
```

## Architecture

This is a Python CLI application built with Click framework using modern Python packaging standards.

**Project Structure:**
- `src/commitcurry/` - Main application package using src-layout
- `src/commitcurry/main.py` - CLI entry point with Click commands
- `tests/` - Test suite using pytest
- `pyproject.toml` - Modern Python packaging configuration

**Key Technologies:**
- **CLI Framework:** Click for command-line interface
- **Build System:** Hatchling (PEP 517/518 compliant)
- **Testing:** pytest with coverage reporting
- **Linting:** Ruff for fast Python linting and formatting
- **Type Checking:** mypy with strict configuration

**Entry Points:**
The main CLI command is defined in `pyproject.toml` as:
```toml
[project.scripts]
commitcurry = "commitcurry.main:main"
```

**Development Configuration:**
- Coverage reports generated in `htmlcov/` directory
- Ruff configured for Python 3.8+ with comprehensive rule set
- mypy configured with strict type checking (`disallow_untyped_defs = true`)
- pytest configured with automatic coverage collection