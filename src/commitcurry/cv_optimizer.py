"""CV optimization module using various AI agents."""

from pathlib import Path

from griptape.structures import Agent  # type: ignore


class CVOptimizer:
    """CV optimization service using configurable AI agents."""

    def __init__(self, agent: Agent):
        """Initialize the CV optimizer.

        Args:
            agent: AI agent instance to use for optimization
        """
        self.agent = agent
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

            # Use the configured agent to generate optimized CV
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
                f"Failed to optimize CV with agent: {str(e)}"
            ) from e


def create_cv_optimizer(agent: Agent) -> CVOptimizer:
    """Factory function to create a CV optimizer instance.
    
    Args:
        agent: AI agent instance to use for optimization
        
    Returns:
        CVOptimizer instance configured with the given agent
    """
    return CVOptimizer(agent=agent)
