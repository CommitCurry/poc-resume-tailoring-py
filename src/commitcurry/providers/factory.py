"""Agent factory for creating AI agent instances with prompt drivers."""

import os
from typing import Any

from griptape.drivers.prompt.google import GooglePromptDriver  # type: ignore
from griptape.drivers.prompt.ollama import OllamaPromptDriver  # type: ignore
from griptape.structures import Agent  # type: ignore


class AgentFactory:
    """Factory for creating AI agent instances with prompt drivers."""

    @classmethod
    def create_agent(cls, model_name: str, **kwargs: Any) -> Agent:
        """Create an AI agent instance based on the model name prefix.

        Args:
            model_name: The model identifier with format:
                - 'gemini-*' for Gemini models (e.g., 'gemini-2.5-flash')
                - 'ollama:*' for Ollama models (e.g., 'ollama:qwen3:8b')
            **kwargs: Additional arguments passed to prompt driver configuration

        Returns:
            Agent instance configured with the appropriate prompt driver

        Raises:
            ValueError: If model format is not supported
            ConnectionError: If connection to the service fails
        """
        prompt_driver = cls._create_prompt_driver(model_name, **kwargs)
        return Agent(prompt_driver=prompt_driver)

    @classmethod
    def _create_prompt_driver(cls, model_name: str, **kwargs: Any) -> Any:
        """Create a prompt driver based on the model name prefix.

        Args:
            model_name: The model identifier
            **kwargs: Additional arguments passed to prompt driver configuration

        Returns:
            Configured prompt driver instance (GooglePromptDriver or OllamaPromptDriver)

        Raises:
            ValueError: If model format is not supported
            ConnectionError: If connection to the service fails
        """
        if model_name.startswith("gemini"):
            # Gemini models: gemini-2.5-flash, gemini-1.5-pro, etc.
            api_key = kwargs.get("api_key") or os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError(
                    "Gemini API key is required. Set GEMINI_API_KEY environment "
                    "variable or pass api_key parameter."
                )

            try:
                return GooglePromptDriver(model=model_name, api_key=api_key)
            except Exception as e:
                raise Exception(
                    f"Failed to create Gemini prompt driver for model "
                    f"'{model_name}': {str(e)}"
                ) from e

        elif model_name.startswith("ollama:"):
            # Ollama models: ollama:qwen3:8b, ollama:mistral:7b, etc.
            # Extract actual model name after "ollama:" prefix
            actual_model_name = model_name[7:]  # Remove "ollama:" prefix
            if not actual_model_name:
                raise ValueError(
                    f"Invalid Ollama model format: '{model_name}'. "
                    "Expected format: 'ollama:model_name' (e.g., 'ollama:qwen3:8b')"
                )

            # Get base_url from kwargs or environment, with localhost fallback
            base_url = (
                kwargs.get("base_url")
                or os.getenv("OLLAMA_URL")
                or "http://localhost:11434"
            ).rstrip("/")

            try:
                return OllamaPromptDriver(model=actual_model_name, host=base_url)
            except Exception as e:
                raise ConnectionError(
                    f"Failed to create Ollama prompt driver for '{actual_model_name}' "
                    f"at {base_url}. Make sure Ollama is running with "
                    f"'ollama serve' and the model is available. "
                    f"Run 'ollama pull {actual_model_name}' if needed. Error: {str(e)}"
                ) from e

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
