from functools import lru_cache
from app.services.input_service.input_layer import InputService
from app.services.llm_service.llm_service import LLMService
from app.services.llm_service.providers.gemini_provider import GeminiLLMProvider
from app.services.tts_service.tts_service import TTSService
from app.services.tts_service.providers.hume_provider import HumeTTSProvider
from app.core.config import settings

@lru_cache()
def get_input_service() -> InputService:
    return InputService()

@lru_cache()
def get_llm_service() -> LLMService:
    provider = GeminiLLMProvider(api_key=settings.gemini_api_key)
    return LLMService(provider=provider)

@lru_cache()
def get_tts_service() -> TTSService:
    provider = HumeTTSProvider(api_key=settings.hume_api_key)
    return TTSService(provider=provider)
