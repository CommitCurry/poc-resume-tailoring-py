"""Ollama prompt driver provider using Griptape."""

import os
from typing import Optional

from griptape.drivers.prompt.ollama import OllamaPromptDriver  # type: ignore

from .base import PromptDriverProvider


class OllamaProvider(PromptDriverProvider):
    """Ollama prompt driver provider using Ollama API."""

    def __init__(self, model_name: str, base_url: Optional[str] = None):
        """Initialize the Ollama provider.

        Args:
            model_name: The Ollama model name (e.g., 'qwen3:8b')
            base_url: The base URL for Ollama API. If None, will be read from
                OLLAMA_URL env var.
        """
        self._model_name = model_name
        self.base_url = (base_url or os.getenv("OLLAMA_URL") or "http://localhost:11434").rstrip("/")

    def create_prompt_driver(self) -> OllamaPromptDriver:
        """Create and configure an Ollama prompt driver instance.
        
        Returns:
            Configured OllamaPromptDriver instance
            
        Raises:
            ConnectionError: If driver creation fails
        """
        try:
            return OllamaPromptDriver(
                model=self._model_name,
                host=self.base_url
            )
        except Exception as e:
            raise ConnectionError(
                f"Failed to create Ollama prompt driver for '{self._model_name}' "
                f"at {self.base_url}. Make sure Ollama is running with "
                f"'ollama serve' and the model is available. "
                f"Run 'ollama pull {self._model_name}' if needed. Error: {str(e)}"
            ) from e

    @property
    def provider_name(self) -> str:
        """Return the provider name identifier."""
        return "ollama"

    @property
    def model_name(self) -> str:
        """Return the model name identifier."""
        return self._model_name
