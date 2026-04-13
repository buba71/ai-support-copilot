import os 
from openai import OpenAI
from dotenv import load_dotenv

from ai_service.core.schemas.llm import LLMResponse
from ai_service.retry.retry_service import RetryService

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.retry = RetryService()

    def ask(self, messages: list[dict], temperature: float = 0.2) -> LLMResponse: 

        response = self.retry.execute(
            self.client.chat.completions.create,
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        return LLMResponse(
            response=response.choices[0].message.content or "",
            tokens_input=response.usage.prompt_tokens,
            tokens_output=response.usage.completion_tokens,
            model=response.model,
        )