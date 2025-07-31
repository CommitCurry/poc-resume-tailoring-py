"""Main entry point for CommitCurry CLI application."""

import sys
from pathlib import Path
from typing import Optional

import click

from .cv_optimizer import create_cv_optimizer


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
def main(cv_file: Path, job_file: Path) -> None:
    """CommitCurry - AI-powered resume tailoring tool.

    CV_FILE: Path to the CV/resume file
    JOB_FILE: Path to the job description file
    """
    # Read file contents
    cv_content = read_file_content(cv_file)
    job_content = read_file_content(job_file)

    try:
        # Initialize CV optimizer
        click.echo("🤖 Initializing CV optimizer...")
        optimizer = create_cv_optimizer()

        # Optimize the CV
        click.echo("✨ Optimizing CV for the job description...")
        optimized_cv = optimizer.optimize_cv(cv_content, job_content)

        # Print the optimized CV
        click.echo("\n" + "=" * 60)
        click.echo("🎯 OPTIMIZED CV")
        click.echo("=" * 60)
        click.echo(optimized_cv)

    except ValueError as e:
        click.echo(f"❌ Configuration Error: {e}", err=True)
        click.echo("💡 Tip: Set your GEMINI_API_KEY environment variable", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Optimization failed: {e}", err=True)
        click.echo("\n📄 Falling back to original CV:", err=True)
        click.echo("=" * 50)
        click.echo(cv_content)
        sys.exit(1)


if __name__ == "__main__":
    main()
