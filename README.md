# CommitCurry

AI-powered resume tailoring tool that optimizes CVs for specific job descriptions using either cloud-based Gemini or local models via Ollama.

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

### Option 1: Gemini (Cloud)

**Gemini API Key**: Set your API key as an environment variable:

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Option 2: Local Models with Ollama

**Install Ollama** (one-time setup):

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download
```

**Download recommended models** (one-time per model):

```bash
# Choose one or all of these models for local experimentation
ollama pull qwen2.5:7b     # ~4.1GB - Excellent text quality, reasoning
ollama pull llama3.1:8b    # ~4.7GB - Balanced performance and efficiency  
ollama pull mistral:7b     # ~4.1GB - Professional writing, structured output
```

**Start Ollama server**:

```bash
ollama serve  # Keep running in background, starts on http://localhost:11434
```

**Verify setup**:

```bash
ollama list           # Show downloaded models
ollama run qwen2.5:7b # Test a model (type /bye to exit)
```

**Storage requirements**: ~12-15GB total for all three models.

## Usage

```bash
# Basic usage (uses Gemini by default)
uv run commitcurry cv.md job.md

# Specify model with -m flag
uv run commitcurry -m gemini-2.5-flash cv.md job.md
uv run commitcurry -m ollama:qwen2.5:7b cv.md job.md

# Verbose output (shows progress messages)
uv run commitcurry -v -m ollama:qwen2.5:7b cv.md job.md

# Example with sample files
uv run commitcurry samples/cv.md samples/job.md
uv run commitcurry -m ollama:qwen2.5:7b samples/cv.md samples/job.md
```

### Model Selection

Use the `-m` or `--model` flag to choose your AI model:

**Cloud Models (require API key):**
- `gemini-2.5-flash` (default) - Latest Gemini model
- `gemini-2.0-flash` - Previous Gemini version
- `gemini-1.5-flash` - Older Gemini version

**Local Models (require Ollama):**
- `ollama:qwen2.5:7b` - Excellent for multilingual resume writing
- `ollama:deepseek-r1:7b` - Advanced reasoning for complex optimization
- `ollama:llama3.3:8b` - Balanced performance and quality
- `ollama:mistral:7b` - Professional writing specialist
- `ollama:phi4:14b` - Compact reasoning model
- `ollama:gemma2:9b` - Efficient Google model

The application will:
1. Read your CV and job description files
2. Use AI (Gemini or local Ollama models) to optimize your CV for the specific job
3. Output the tailored resume to stdout

**Output modes:**
- **Quiet mode** (default): Only outputs the optimized CV content
- **Verbose mode** (`-v` or `--verbose`): Shows progress messages and formatting

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