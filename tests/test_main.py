"""Tests for the main module."""

from click.testing import CliRunner

from commitcurry.main import main


def test_main_command() -> None:
    """Test that the main command prints the expected message."""
    runner = CliRunner()
    result = runner.invoke(main)

    assert result.exit_code == 0
    assert "Hello, I'm CommitCurry" in result.output
