"""Tests for the CV optimizer module."""


import pytest

from commitcurry.cv_optimizer import CVOptimizer, create_cv_optimizer
from commitcurry.models.base import AIModel


class MockAIModel(AIModel):
    """Mock AI model for testing."""

    def __init__(self, model_name: str = "mock-model"):
        self._model_name = model_name
        self.generate_response = "Mocked optimized CV response"
        self.generate_calls = []

    def generate(self, prompt: str) -> str:
        self.generate_calls.append(prompt)
        return self.generate_response

    @property
    def model_name(self) -> str:
        return self._model_name


def test_cv_optimizer_init():
    """Test CVOptimizer initialization with a model."""
    mock_model = MockAIModel("test-model")
    optimizer = CVOptimizer(model=mock_model)
    assert optimizer.model == mock_model
    assert optimizer.model.model_name == "test-model"


def test_cv_optimizer_prompt_template_loading():
    """Test that the prompt template is loaded correctly."""
    mock_model = MockAIModel()
    optimizer = CVOptimizer(model=mock_model)
    assert optimizer.prompt_template is not None
    assert "optimize" in optimizer.prompt_template.lower()
    assert "{cv_content}" in optimizer.prompt_template
    assert "{job_description}" in optimizer.prompt_template


def test_optimize_cv_success():
    """Test successful CV optimization."""
    mock_model = MockAIModel("test-model")
    mock_model.generate_response = "Optimized CV content here"

    optimizer = CVOptimizer(model=mock_model)
    result = optimizer.optimize_cv("Original CV", "Job Description")

    assert result == "Optimized CV content here"
    assert len(mock_model.generate_calls) == 1

    # Check that the prompt was formatted correctly
    generated_prompt = mock_model.generate_calls[0]
    assert "Original CV" in generated_prompt
    assert "Job Description" in generated_prompt


def test_optimize_cv_failure():
    """Test CV optimization failure handling."""
    mock_model = MockAIModel("error-model")

    # Make the mock model raise an exception
    def failing_generate(prompt: str) -> str:
        raise Exception("Model API Error")

    mock_model.generate = failing_generate

    optimizer = CVOptimizer(model=mock_model)

    with pytest.raises(
        Exception, match="Failed to optimize CV with error-model: Model API Error"
    ):
        optimizer.optimize_cv("Original CV", "Job Description")


def test_create_cv_optimizer_factory():
    """Test the factory function."""
    mock_model = MockAIModel("factory-test")
    optimizer = create_cv_optimizer(mock_model)

    assert isinstance(optimizer, CVOptimizer)
    assert optimizer.model == mock_model
    assert optimizer.model.model_name == "factory-test"


def test_cv_optimizer_strips_content():
    """Test that CV optimizer strips whitespace from input content."""
    mock_model = MockAIModel()
    optimizer = CVOptimizer(model=mock_model)

    # Test with content that has leading/trailing whitespace
    optimizer.optimize_cv("  Original CV  ", "  Job Description  ")

    # Check that the prompt received stripped content
    generated_prompt = mock_model.generate_calls[0]
    # The template should contain the stripped content
    assert "Original CV" in generated_prompt
    assert "Job Description" in generated_prompt
    # Should not contain the extra spaces
    assert "  Original CV  " not in generated_prompt
    assert "  Job Description  " not in generated_prompt
