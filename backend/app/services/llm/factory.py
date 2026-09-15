from app.services.llm.base import LLMClient
from app.services.llm.groq_client import GroqClient


def get_llm_client() -> LLMClient:
    return GroqClient()