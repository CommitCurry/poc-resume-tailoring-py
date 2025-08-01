"""Tests for the main module."""

import os
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from commitcurry.main import main


def test_main_command_with_valid_files_no_api_key(tmp_path: Path) -> None:
    """Test that the main command fails gracefully without API key."""
    # Create temporary test files
    cv_file = tmp_path / "test_cv.txt"
    job_file = tmp_path / "test_job.txt"

    cv_content = "John Doe\nSoftware Engineer\nExperience: 5 years"
    job_content = "Senior Developer Position\nRequirements: Python, 3+ years"

    cv_file.write_text(cv_content)
    job_file.write_text(job_content)

    runner = CliRunner()
    result = runner.invoke(main, [str(cv_file), str(job_file)])

    # Should fail due to missing API key
    assert result.exit_code == 1
    assert "Configuration Error" in result.output
    assert "GEMINI_API_KEY" in result.output
    # Should not show verbose tip in quiet mode
    assert "💡 Tip:" not in result.output


@patch("commitcurry.main.ModelFactory.create_model")
@patch("commitcurry.main.create_cv_optimizer")
def test_main_command_with_valid_files_and_api_key(
    mock_create_optimizer, mock_create_model, tmp_path: Path
) -> None:
    """Test that the main command works with valid files and API key (quiet mode)."""
    # Mock the model and optimizer
    mock_model = mock_create_model.return_value
    mock_optimizer = mock_create_optimizer.return_value
    mock_optimizer.optimize_cv.return_value = "Optimized CV content"

    # Create temporary test files
    cv_file = tmp_path / "test_cv.txt"
    job_file = tmp_path / "test_job.txt"

    cv_content = "John Doe\nSoftware Engineer\nExperience: 5 years"
    job_content = "Senior Developer Position\nRequirements: Python, 3+ years"

    cv_file.write_text(cv_content)
    job_file.write_text(job_content)

    runner = CliRunner()
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
        result = runner.invoke(main, [str(cv_file), str(job_file)])

    assert result.exit_code == 0
    # In quiet mode, should only show the optimized CV content
    assert "Optimized CV content" in result.output
    # Should not show verbose messages in quiet mode
    assert "🤖 Initializing" not in result.output
    assert "✨ Optimizing" not in result.output
    assert "🎯 OPTIMIZED CV" not in result.output
    mock_optimizer.optimize_cv.assert_called_once_with(cv_content, job_content)
    mock_create_model.assert_called_once_with("gemini-2.5-flash")
    mock_create_optimizer.assert_called_once_with(mock_model)


@patch("commitcurry.main.ModelFactory.create_model")
@patch("commitcurry.main.create_cv_optimizer")
def test_main_command_verbose_mode(
    mock_create_optimizer, mock_create_model, tmp_path: Path
) -> None:
    """Test that the main command shows progress messages in verbose mode."""
    # Mock the model and optimizer
    mock_model = mock_create_model.return_value
    mock_optimizer = mock_create_optimizer.return_value
    mock_optimizer.optimize_cv.return_value = "Optimized CV content"

    # Create temporary test files
    cv_file = tmp_path / "test_cv.txt"
    job_file = tmp_path / "test_job.txt"

    cv_content = "John Doe\nSoftware Engineer\nExperience: 5 years"
    job_content = "Senior Developer Position\nRequirements: Python, 3+ years"

    cv_file.write_text(cv_content)
    job_file.write_text(job_content)

    runner = CliRunner()
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
        result = runner.invoke(main, ["-v", str(cv_file), str(job_file)])

    assert result.exit_code == 0
    # In verbose mode, should show progress messages
    assert "🤖 Initializing gemini-2.5-flash model..." in result.output
    assert "✨ Optimizing CV for the job description..." in result.output
    assert "🎯 OPTIMIZED CV" in result.output
    assert "Optimized CV content" in result.output
    mock_optimizer.optimize_cv.assert_called_once_with(cv_content, job_content)
    mock_create_model.assert_called_once_with("gemini-2.5-flash")
    mock_create_optimizer.assert_called_once_with(mock_model)


def test_main_command_verbose_mode_no_api_key(tmp_path: Path) -> None:
    """Test verbose mode shows tip when API key is missing."""
    # Create temporary test files
    cv_file = tmp_path / "test_cv.txt"
    job_file = tmp_path / "test_job.txt"

    cv_content = "John Doe\nSoftware Engineer\nExperience: 5 years"
    job_content = "Senior Developer Position\nRequirements: Python, 3+ years"

    cv_file.write_text(cv_content)
    job_file.write_text(job_content)

    runner = CliRunner()
    result = runner.invoke(main, ["--verbose", str(cv_file), str(job_file)])

    # Should fail due to missing API key
    assert result.exit_code == 1
    assert "Configuration Error" in result.output
    assert "GEMINI_API_KEY" in result.output


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
