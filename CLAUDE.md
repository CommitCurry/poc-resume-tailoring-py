# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Management

**Python Version Management:**
- **uv**: Modern Python package manager and environment tool

**Setup:**
```bash
# Create virtual environment and install dependencies
uv sync

# Install project with dev dependencies
uv pip install -e ".[dev]"
```

## Development Commands

**Installation:**
```bash
uv sync
```

**Running the application:**
```bash
uv run commitcurry             # Recommended method
uv run python -m commitcurry.main # Alternative method
```

**Testing:**
```bash
uv run pytest                  # Run all tests with coverage
uv run pytest tests/test_main.py # Run specific test file
uv run pytest -v               # Verbose output
```

**Code Quality:**
```bash
uv run ruff check .            # Lint code
uv run ruff format .           # Format code
uv run ruff check --fix .      # Auto-fix linting issues
uv run mypy src/               # Type checking
```

**Environment Commands:**
```bash
uv sync                        # Sync project dependencies
uv add <package>               # Add runtime dependency
uv add --dev <package>         # Add development dependency
uv remove <package>            # Remove dependency
```

**Run All Validations:**
```bash
./validate                     # Run all checks (tests, lint, format, types)
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