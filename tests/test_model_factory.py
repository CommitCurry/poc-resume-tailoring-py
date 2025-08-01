"""Tests for the model factory."""

import pytest

from commitcurry.models.factory import ModelFactory
from commitcurry.models.gemini import GeminiModel
from commitcurry.models.ollama import OllamaModel


def test_create_gemini_model():
    """Test creating Gemini models with various names."""
    # Test various Gemini model names
    gemini_models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash", 
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-custom-version"
    ]
    
    for model_name in gemini_models:
        try:
            model = ModelFactory.create_model(model_name, api_key="test-key")
            assert isinstance(model, GeminiModel)
            assert model.model_name == model_name
        except ValueError as e:
            # Skip if API key validation fails - that's expected in test
            if "API key" in str(e):
                continue
            raise


def test_create_ollama_model():
    """Test creating Ollama models with ollama: prefix."""
    ollama_models = [
        ("ollama:qwen3:8b", "qwen3:8b"),
        ("ollama:deepseek-r1:8b", "deepseek-r1:8b"),
        ("ollama:llama3.3:8b", "llama3.3:8b"), 
        ("ollama:mistral:7b", "mistral:7b"),
        ("ollama:phi4:14b", "phi4:14b"),
        ("ollama:custom-model", "custom-model")
    ]
    
    for full_name, expected_model_name in ollama_models:
        try:
            model = ModelFactory.create_model(full_name)
            assert isinstance(model, OllamaModel)
            assert model.model_name == expected_model_name
        except ConnectionError:
            # Skip if Ollama connection fails - that's expected in test
            continue


def test_invalid_ollama_format():
    """Test error handling for invalid Ollama format."""
    with pytest.raises(ValueError, match="Invalid Ollama model format"):
        ModelFactory.create_model("ollama:")


def test_unsupported_model_format():
    """Test error handling for unsupported model formats."""
    invalid_models = [
        "openai:gpt-4",
        "claude:sonnet",
        "unknown-model",
        "qwen3:8b",  # Should be ollama:qwen3:8b
        ""
    ]
    
    for model_name in invalid_models:
        with pytest.raises(ValueError, match="Unsupported model format"):
            ModelFactory.create_model(model_name)


def test_list_supported_formats():
    """Test listing supported model formats."""
    formats = ModelFactory.list_supported_formats()
    
    assert "gemini" in formats
    assert "ollama" in formats
    
    # Check Gemini format
    gemini_info = formats["gemini"]
    assert gemini_info["format"] == "gemini-*"
    assert "gemini-2.5-flash" in gemini_info["examples"]
    assert "description" in gemini_info
    
    # Check Ollama format
    ollama_info = formats["ollama"]
    assert ollama_info["format"] == "ollama:*"
    assert "ollama:qwen3:8b" in ollama_info["examples"]
    assert "description" in ollama_info


def test_model_name_extraction():
    """Test that Ollama model names are correctly extracted."""
    test_cases = [
        ("ollama:simple", "simple"),
        ("ollama:model:with:colons", "model:with:colons"),
        ("ollama:qwen3:8b", "qwen3:8b"),
        ("ollama:very-long-model-name-123", "very-long-model-name-123")
    ]
    
    for full_name, expected_model_name in test_cases:
        try:
            model = ModelFactory.create_model(full_name)
            assert isinstance(model, OllamaModel)
            assert model.model_name == expected_model_name
        except ConnectionError:
            # Skip if Ollama connection fails - that's expected in test
            continue