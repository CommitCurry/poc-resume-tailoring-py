# CommitCurry

A command line application for CommitCurry.

## Prerequisites

**Install uv** (handles Python versions and packages automatically):

```bash
# macOS
brew install uv

# Other platforms: see https://docs.astral.sh/uv/getting-started/installation/
```

## Installation

```bash
# Install project with development dependencies (uv handles everything automatically)
uv pip install -e ".[dev]"
```

## Usage

```bash
# Run the application (no manual environment activation needed)
uv run commitcurry
```

## Development

### Running Tests
```bash
uv run pytest                    # Run all tests
uv run pytest tests/test_main.py # Run specific test
uv run pytest -v                 # Verbose output
```

### Code Quality
```bash
uv run ruff check .              # Lint code
uv run ruff format .             # Format code
uv run ruff check --fix .        # Auto-fix issues
uv run mypy src/                 # Type checking
```

### Adding Dependencies
```bash
uv add <package-name>            # Add runtime dependency
uv add --dev <package-name>      # Add development dependency
```

### Run All Validations
```bash
./validate
```

### Development Workflow
```bash
# One-time setup
uv pip install -e ".[dev]"

# Daily development - no manual activation needed!
uv run commitcurry               # Test the app
uv run pytest                    # Run tests
uv run ruff check --fix .        # Lint and fix
uv run mypy src/                 # Type check

# Before committing - run all validations
./validate
```