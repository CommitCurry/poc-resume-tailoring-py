"""Tests for the main module."""

from pathlib import Path

from click.testing import CliRunner

from commitcurry.main import main


def test_main_command_with_valid_files(tmp_path: Path) -> None:
    """Test that the main command works with valid CV and job files."""
    # Create temporary test files
    cv_file = tmp_path / "test_cv.txt"
    job_file = tmp_path / "test_job.txt"

    cv_content = "John Doe\nSoftware Engineer\nExperience: 5 years"
    job_content = "Senior Developer Position\nRequirements: Python, 3+ years"

    cv_file.write_text(cv_content)
    job_file.write_text(job_content)

    runner = CliRunner()
    result = runner.invoke(main, [str(cv_file), str(job_file)])

    assert result.exit_code == 0
    assert "CV Content:" in result.output
    assert cv_content in result.output


def test_main_command_missing_arguments() -> None:
    """Test that the command fails when arguments are missing."""
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code != 0
    assert "Missing argument" in result.output


def test_main_command_nonexistent_cv_file(tmp_path: Path) -> None:
    """Test that the command fails when CV file doesn't exist."""
    job_file = tmp_path / "test_job.txt"
    job_file.write_text("Job description")

    runner = CliRunner()
    result = runner.invoke(main, ["nonexistent_cv.txt", str(job_file)])

    assert result.exit_code != 0
    assert "File does not exist" in result.output


def test_main_command_nonexistent_job_file(tmp_path: Path) -> None:
    """Test that the command fails when job file doesn't exist."""
    cv_file = tmp_path / "test_cv.txt"
    cv_file.write_text("CV content")

    runner = CliRunner()
    result = runner.invoke(main, [str(cv_file), "nonexistent_job.txt"])

    assert result.exit_code != 0
    assert "File does not exist" in result.output


def test_main_command_directory_instead_of_file(tmp_path: Path) -> None:
    """Test that the command fails when a directory is passed instead of a file."""
    job_file = tmp_path / "test_job.txt"
    job_file.write_text("Job description")

    directory = tmp_path / "test_dir"
    directory.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [str(directory), str(job_file)])

    assert result.exit_code != 0
    assert "Path is not a file" in result.output
