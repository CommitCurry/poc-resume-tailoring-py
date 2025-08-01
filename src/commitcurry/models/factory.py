"""Model factory for creating AI model instances."""

from .base import AIModel
from .gemini import GeminiModel
from .ollama import OllamaModel


class ModelFactory:
    """Factory for creating AI model instances using prefix-based detection."""

    @classmethod
    def create_model(cls, model_name: str, **kwargs) -> AIModel:
        """Create an AI model instance based on the model name prefix.

        Args:
            model_name: The model identifier with format:
                - 'gemini-*' for Gemini models (e.g., 'gemini-2.5-flash')
                - 'ollama:*' for Ollama models (e.g., 'ollama:qwen3:8b')
            **kwargs: Additional arguments passed to model constructor

        Returns:
            AIModel instance

        Raises:
            ValueError: If model format is not supported
        """
        if model_name.startswith("gemini"):
            # Gemini models: gemini-2.5-flash, gemini-1.5-pro, etc.
            api_key = kwargs.get("api_key")
            return GeminiModel(model_name=model_name, api_key=api_key)

        elif model_name.startswith("ollama:"):
            # Ollama models: ollama:qwen3:8b, ollama:mistral:7b, etc.
            # Extract actual model name after "ollama:" prefix
            actual_model_name = model_name[7:]  # Remove "ollama:" prefix
            if not actual_model_name:
                raise ValueError(
                    f"Invalid Ollama model format: '{model_name}'. "
                    "Expected format: 'ollama:model_name' (e.g., 'ollama:qwen3:8b')"
                )
            
            base_url = kwargs.get("base_url", "http://localhost:11434")
            return OllamaModel(model_name=actual_model_name, base_url=base_url)

        else:
            raise ValueError(
                f"Unsupported model format: '{model_name}'. "
                f"Supported formats:\n"
                f"  - Gemini: 'gemini-*' (e.g., 'gemini-2.5-flash')\n"
                f"  - Ollama: 'ollama:*' (e.g., 'ollama:qwen3:8b')"
            )

    @classmethod
    def list_supported_formats(cls) -> dict:
        """List supported model formats and examples.

        Returns:
            Dictionary with format information and examples
        """
        return {
            "gemini": {
                "format": "gemini-*",
                "examples": [
                    "gemini-2.5-flash",
                    "gemini-2.0-flash", 
                    "gemini-1.5-flash",
                    "gemini-1.5-pro"
                ],
                "description": "Google Gemini models (requires API key)"
            },
            "ollama": {
                "format": "ollama:*",
                "examples": [
                    "ollama:qwen3:8b",
                    "ollama:deepseek-r1:8b",
                    "ollama:llama3.3:8b",
                    "ollama:mistral:7b",
                    "ollama:phi4:14b"
                ],
                "description": "Local Ollama models (requires Ollama server)"
            }
        }
