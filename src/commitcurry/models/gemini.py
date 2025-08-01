"""Gemini model implementation using Griptape."""

import os
from typing import Optional

from griptape.drivers.prompt.google import GooglePromptDriver  # type: ignore
from griptape.structures import Agent  # type: ignore

from .base import AIModel


class GeminiModel(AIModel):
    """Gemini model implementation using Griptape and Google AI."""

    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """Initialize the Gemini model.

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

        # Configure Griptape with Gemini
        self.prompt_driver = GooglePromptDriver(
            model=model_name, api_key=self.api_key
        )

        # Create agent with the configured driver
        self.agent = Agent(prompt_driver=self.prompt_driver)

    def generate(self, prompt: str) -> str:
        """Generate text using Gemini model.

        Args:
            prompt: The input prompt for text generation

        Returns:
            Generated text response

        Raises:
            Exception: If generation fails
        """
        try:
            # Run the generation
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
            raise Exception(f"Failed to generate with Gemini: {str(e)}") from e

    @property
    def model_name(self) -> str:
        """Return the model name identifier."""
        return self._model_name
