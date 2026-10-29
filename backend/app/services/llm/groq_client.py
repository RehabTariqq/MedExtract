from groq import Groq

from app.core.config import GROQ_API_KEY, GROQ_MODEL
from app.services.llm.base import LLMClient

_client: Groq | None = None


def get_groq() -> Groq:
    """Create the Groq client lazily so a missing key gives a clear error, not an import crash."""
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not set. Add it to backend/.env (or your Render env vars).")
        _client = Groq(api_key=GROQ_API_KEY, timeout=60.0, max_retries=3)
    return _client


class GroqClient(LLMClient):
    def generate(self, prompt: str) -> str:
        response = get_groq().chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            reasoning_effort="low",  # gpt-oss is a reasoning model; "low" keeps extraction fast
        )
        return response.choices[0].message.content or ""
