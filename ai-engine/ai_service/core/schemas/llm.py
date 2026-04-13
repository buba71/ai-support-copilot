from pydantic import BaseModel

class LLMResponse(BaseModel):
    response: str
    tokens_input: int
    tokens_output: int
    model: str