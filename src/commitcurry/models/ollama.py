"""Ollama model implementation using Griptape."""

import os
from typing import Optional

from griptape.drivers.prompt.ollama import OllamaPromptDriver  # type: ignore
from griptape.structures import Agent  # type: ignore

from .base import AIModel


class OllamaModel(AIModel):
    """Ollama model implementation using Griptape and Ollama."""

    def __init__(self, model_name: str, base_url: Optional[str] = None):
        """Initialize the Ollama model.

        Args:
            model_name: The Ollama model name (e.g., 'qwen3:8b')
            base_url: The base URL for Ollama API. If None, will be read from
                OLLAMA_URL env var.
        """
        self._model_name = model_name
        self.base_url = (base_url or os.getenv("OLLAMA_URL") or "http://localhost:11434").rstrip("/")

        try:
            # Configure Griptape with Ollama
            self.prompt_driver = OllamaPromptDriver(
                model=model_name,
                host=self.base_url
            )

            # Create agent with the configured driver
            self.agent = Agent(prompt_driver=self.prompt_driver)

        except Exception as e:
            raise ConnectionError(
                f"Failed to initialize Ollama connection to {base_url} "
                f"with model '{model_name}'. Make sure Ollama is running with "
                f"'ollama serve' and the model is available. "
                f"Run 'ollama pull {model_name}' if needed. Error: {str(e)}"
            ) from e

    def generate(self, prompt: str) -> str:
        """Generate text using Ollama model via Griptape.

        Args:
            prompt: The input prompt for text generation

        Returns:
            Generated text response

        Raises:
            Exception: If generation fails
        """
        try:
            # Run the generation using Griptape Agent
            response = self.agent.run(prompt)

            # Extract the output text from Griptape Agent response
            if hasattr(response, "output_task") and hasattr(
                response.output_task, "output"
            ):
                # For newer Griptape versions
                output_value = response.output_task.output
                if hasattr(output_value, "value"):
                    return str(output_value.value).strip()
                else:
                    return str(output_value).strip()
            elif hasattr(response, "output"):
                # Alternative structure
                output_value = response.output
                if hasattr(output_value, "value"):
                    return str(output_value.value).strip()
                else:
                    return str(output_value).strip()
            else:
                # Fallback - convert response to string
                return str(response).strip()

        except Exception as e:
            raise Exception(
                f"Failed to generate with Ollama model '{self._model_name}': {str(e)}"
            ) from e

    @property
    def model_name(self) -> str:
        """Return the model name identifier."""
        return self._model_name
