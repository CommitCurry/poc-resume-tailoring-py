"""Main entry point for CommitCurry CLI application."""

import sys
from pathlib import Path
from typing import Optional

import click

from .config.logging import setup_logging
from .cv_optimizer import create_cv_optimizer
from .providers.factory import AgentFactory


def read_file_content(file_path: Path) -> str:
    """Read content from a file with error handling."""
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        click.echo(f"Error: File not found: {file_path}", err=True)
        sys.exit(1)
    except PermissionError:
        click.echo(f"Error: Permission denied reading file: {file_path}", err=True)
        sys.exit(1)
    except UnicodeDecodeError:
        click.echo(f"Error: Unable to decode file as UTF-8: {file_path}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error reading file {file_path}: {e}", err=True)
        sys.exit(1)


def validate_file_path(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> Optional[Path]:
    """Validate that the file path exists and is a file."""
    if value is None:
        return None

    file_path = Path(value)

    if not file_path.exists():
        raise click.BadParameter(f"File does not exist: {file_path}")

    if not file_path.is_file():
        raise click.BadParameter(f"Path is not a file: {file_path}")

    return file_path


@click.command()
@click.argument("cv_file", callback=validate_file_path, type=str)
@click.argument("job_file", callback=validate_file_path, type=str)
@click.option(
    "-m", "--model",
    default="gemini-2.5-flash",
    help="AI model to use (e.g., 'gemini-2.5-flash', 'ollama:qwen3:8b')"
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Show progress messages and formatting"
)
def main(cv_file: Path, job_file: Path, model: str, verbose: bool) -> None:
    """CommitCurry - AI-powered resume tailoring tool.

    CV_FILE: Path to the CV/resume file
    JOB_FILE: Path to the job description file
    """
    # Configure logging early to capture all library logs
    setup_logging()

    # Read file contents
    cv_content = read_file_content(cv_file)
    job_content = read_file_content(job_file)

    try:
        # Create AI agent instance
        if verbose:
            click.echo(f"🤖 Initializing {model} agent...")
        agent = AgentFactory.create_agent(model)

        # Initialize CV optimizer with the agent
        optimizer = create_cv_optimizer(agent)

        # Optimize the CV
        if verbose:
            click.echo("✨ Optimizing CV for the job description...")
        optimized_cv = optimizer.optimize_cv(cv_content, job_content)

        # Print the optimized CV
        if verbose:
            click.echo("\n" + "=" * 60)
            click.echo("🎯 OPTIMIZED CV")
            click.echo("=" * 60)
        click.echo(optimized_cv)

    except ValueError as e:
        click.echo(f"❌ Configuration Error: {e}", err=True)
        sys.exit(1)
    except ConnectionError as e:
        click.echo(f"❌ Connection Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Optimization failed: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
