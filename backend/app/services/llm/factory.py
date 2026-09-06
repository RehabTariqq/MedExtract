from app.services.llm.base import LLMClient
from app.services.llm.openai_client import OpenAIClient


def get_llm_client() -> LLMClient:
    return OpenAIClient()