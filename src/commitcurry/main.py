"""Main entry point for CommitCurry CLI application."""

import click


@click.command()
def main() -> None:
    """Main entry point for CommitCurry."""
    click.echo("Hello, I'm CommitCurry")


if __name__ == "__main__":
    main()
