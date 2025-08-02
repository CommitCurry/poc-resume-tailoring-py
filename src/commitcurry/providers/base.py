"""Abstract base classes for prompt driver providers."""

from abc import ABC, abstractmethod
from typing import Any


class PromptDriverProvider(ABC):
    """Abstract base class for prompt driver providers."""

    @abstractmethod
    def create_prompt_driver(self) -> Any:
        """Create and configure a prompt driver instance.
        
        Returns:
            Configured prompt driver instance (e.g., GooglePromptDriver,
            OllamaPromptDriver)
            
        Raises:
            Exception: If driver creation fails
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name identifier."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model name identifier."""
        pass
