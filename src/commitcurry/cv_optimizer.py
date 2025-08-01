"""CV optimization module using Griptape and Gemini."""

import os
from pathlib import Path
from typing import Optional

from griptape.drivers.prompt.google import GooglePromptDriver
from griptape.structures import Agent


class CVOptimizer:
    """CV optimization service using Griptape and Gemini."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the CV optimizer.

        Args:
            api_key: Gemini API key. If None, will be read from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Configure Griptape with Gemini
        self.prompt_driver = GooglePromptDriver(
            model="gemini-2.5-flash", api_key=self.api_key
        )

        # Create agent with the configured driver
        self.agent = Agent(prompt_driver=self.prompt_driver)

        # Load prompt template
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        """Load the CV optimization prompt template."""
        template_path = (
            Path(__file__).parent / "templates" / "cv_optimization_prompt.txt"
        )
        try:
            return template_path.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"CV optimization prompt template is required but not found: "
                f"{template_path}. This file should be included as part of the "
                "application package."
            ) from e

    def optimize_cv(self, cv_content: str, job_description: str) -> str:
        """Optimize a CV for a specific job description.

        Args:
            cv_content: The original CV content
            job_description: The job description to tailor the CV for

        Returns:
            The optimized CV content

        Raises:
            Exception: If the optimization fails
        """
        try:
            # Format the prompt with the provided content
            prompt = self.prompt_template.format(
                cv_content=cv_content.strip(), job_description=job_description.strip()
            )

            # Run the optimization
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
            raise Exception(f"Failed to optimize CV: {str(e)}") from e


def create_cv_optimizer() -> CVOptimizer:
    """Factory function to create a CV optimizer instance."""
    return CVOptimizer()
