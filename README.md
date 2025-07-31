# CommitCurry

AI-powered resume tailoring tool that optimizes CVs for specific job descriptions using Gemini.

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

## Configuration

**Gemini API Key**: The application requires a Gemini API key to optimize CVs. Set your API key as an environment variable:

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Usage

```bash
# Run the application with CV and job description files
uv run commitcurry path/to/cv.md path/to/job.md

# Example with sample files
uv run commitcurry samples/cv.md samples/job.md
```

The application will:
1. Read your CV and job description files
2. Use Gemini AI to optimize your CV for the specific job
3. Output the tailored resume to stdout

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