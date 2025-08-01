"""Abstract base classes for AI models."""

from abc import ABC, abstractmethod


class AIModel(ABC):
    """Abstract base class for AI models."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text based on the given prompt.
        
        Args:
            prompt: The input prompt for text generation
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If generation fails
        """
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model name identifier."""
        pass
