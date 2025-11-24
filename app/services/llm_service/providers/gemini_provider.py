import os
from typing import Optional, Any
from app.services.llm_service.gemini_client import GeminiClient, GeminiRequest, GeminiResponse
from app.core.config import settings
from .base import LLMProvider

class GeminiLLMProvider(LLMProvider):
    """Gemini implementation of LLM Provider."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        self.model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

        if not self.api_key:
            raise ValueError("Gemini API key is required.")

        self.client = GeminiClient(self.api_key, self.model_name)

    async def generate_content(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> GeminiResponse:
        request = GeminiRequest(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return await self.client.generate_content(request)

    def parse_response(self, response: GeminiResponse) -> str:
        return response.content
