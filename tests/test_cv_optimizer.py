"""Tests for the CV optimizer module."""

import os
from unittest.mock import Mock, patch

import pytest

from commitcurry.cv_optimizer import CVOptimizer, create_cv_optimizer


def test_cv_optimizer_init_with_api_key():
    """Test CVOptimizer initialization with API key."""
    optimizer = CVOptimizer(api_key="test-api-key")
    assert optimizer.api_key == "test-api-key"


def test_cv_optimizer_init_from_env():
    """Test CVOptimizer initialization from environment variable."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "env-api-key"}):
        optimizer = CVOptimizer()
        assert optimizer.api_key == "env-api-key"


def test_cv_optimizer_init_no_api_key():
    """Test CVOptimizer initialization fails without API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Gemini API key is required"):
            CVOptimizer()


def test_cv_optimizer_prompt_template_loading():
    """Test that the prompt template is loaded correctly."""
    optimizer = CVOptimizer(api_key="test-key")
    assert optimizer.prompt_template is not None
    assert "optimize" in optimizer.prompt_template.lower()
    assert "{cv_content}" in optimizer.prompt_template
    assert "{job_description}" in optimizer.prompt_template


@patch("commitcurry.cv_optimizer.Agent")
@patch("commitcurry.cv_optimizer.GooglePromptDriver")
def test_optimize_cv_success(mock_google_driver, mock_agent_class):
    """Test successful CV optimization."""
    # Mock the agent and its response
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    # Mock response with nested structure
    mock_response = Mock()
    mock_output_task = Mock()
    mock_output = Mock()
    mock_output.value = "Optimized CV content here"
    mock_output_task.output = mock_output
    mock_response.output_task = mock_output_task
    mock_agent.run.return_value = mock_response

    optimizer = CVOptimizer(api_key="test-key")

    result = optimizer.optimize_cv("Original CV", "Job Description")

    assert result == "Optimized CV content here"
    mock_agent.run.assert_called_once()


@patch("commitcurry.cv_optimizer.Agent")
@patch("commitcurry.cv_optimizer.GooglePromptDriver")
def test_optimize_cv_failure(mock_google_driver, mock_agent_class):
    """Test CV optimization failure handling."""
    # Mock the agent to raise an exception
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent
    mock_agent.run.side_effect = Exception("API Error")

    optimizer = CVOptimizer(api_key="test-key")

    with pytest.raises(Exception, match="Failed to optimize CV: API Error"):
        optimizer.optimize_cv("Original CV", "Job Description")


def test_create_cv_optimizer_factory():
    """Test the factory function."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
        optimizer = create_cv_optimizer()
        assert isinstance(optimizer, CVOptimizer)
        assert optimizer.api_key == "test-key"
