from openai import OpenAI
from app.core.config import OPENAI_API_KEY
from app.services.llm.base import LLMClient

_client = OpenAI(api_key=OPENAI_API_KEY)


class OpenAIClient(LLMClient):
    def generate(self, prompt: str) -> str:
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content