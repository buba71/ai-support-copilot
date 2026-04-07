import os 
from openai import OpenAI
from dotenv import load_dotenv
from ai_service.retry.retry_service import RetryService

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.retry = RetryService()

    def ask(self, messages, temperature=0.2) -> dict: 
        
        response = self.retry.execute(
            self.client.chat.completions.create,
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        return {
            "response": response.choices[0].message.content,
            "tokens_input": response.usage.prompt_tokens,
            "tokens_output": response.usage.completion_tokens,
            "model": response.model,
        }