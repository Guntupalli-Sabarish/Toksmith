from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate_content(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> Any:
        """
        Generate content from the LLM.

        Args:
            prompt: The prompt to send.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.

        Returns:
            The raw response from the LLM provider.
        """
        pass

    @abstractmethod
    def parse_response(self, response: Any) -> str:
        """
        Parse the raw response to extract the content string.

        Args:
            response: The raw response from generate_content.

        Returns:
            The extracted content string.
        """
        pass
