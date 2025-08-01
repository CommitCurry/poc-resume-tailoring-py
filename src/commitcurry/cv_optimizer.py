"""CV optimization module using various AI models."""

from pathlib import Path

from .models.base import AIModel


class CVOptimizer:
    """CV optimization service using configurable AI models."""

    def __init__(self, model: AIModel):
        """Initialize the CV optimizer.

        Args:
            model: AI model instance to use for optimization
        """
        self.model = model
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

            # Use the configured model to generate optimized CV
            return self.model.generate(prompt)

        except Exception as e:
            raise Exception(
                f"Failed to optimize CV with {self.model.model_name}: {str(e)}"
            ) from e


def create_cv_optimizer(model: AIModel) -> CVOptimizer:
    """Factory function to create a CV optimizer instance.
    
    Args:
        model: AI model instance to use for optimization
        
    Returns:
        CVOptimizer instance configured with the given model
    """
    return CVOptimizer(model=model)
