from groq import Groq
from app.core.config import GROQ_API_KEY
from app.services.llm.base import LLMClient

_client = Groq(api_key=GROQ_API_KEY)


class GroqClient(LLMClient):
    def generate(self, prompt: str) -> str:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content