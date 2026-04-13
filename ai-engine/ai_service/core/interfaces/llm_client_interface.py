from typing import Any, Protocol
from ai_service.core.schemas.llm import LLMResponse


class LLMClientInterface(Protocol):
    def ask(self, messages: list[dict[str, Any]], temperature: float = 0.2) -> LLMResponse:
        ...