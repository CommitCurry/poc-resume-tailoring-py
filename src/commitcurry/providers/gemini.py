"""Gemini prompt driver provider using Griptape."""

import os
from typing import Optional

from griptape.drivers.prompt.google import GooglePromptDriver  # type: ignore

from .base import PromptDriverProvider


class GeminiProvider(PromptDriverProvider):
    """Gemini prompt driver provider using Google AI API."""

    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """Initialize the Gemini provider.

        Args:
            model_name: The Gemini model name (e.g., 'gemini-2.5-flash')
            api_key: Gemini API key. If None, will be read from GEMINI_API_KEY env var.
        """
        self._model_name = model_name
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

    def create_prompt_driver(self) -> GooglePromptDriver:
        """Create and configure a Google prompt driver instance.
        
        Returns:
            Configured GooglePromptDriver instance
            
        Raises:
            Exception: If driver creation fails
        """
        try:
            return GooglePromptDriver(
                model=self._model_name,
                api_key=self.api_key
            )
        except Exception as e:
            raise Exception(
                f"Failed to create Gemini prompt driver for model "
                f"'{self._model_name}': {str(e)}"
            ) from e

    @property
    def provider_name(self) -> str:
        """Return the provider name identifier."""
        return "gemini"

    @property
    def model_name(self) -> str:
        """Return the model name identifier."""
        return self._model_name
