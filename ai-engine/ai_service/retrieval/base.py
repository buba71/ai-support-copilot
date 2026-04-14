from typing import Protocol

from ai_service.core.schemas.retrieval import RetrievedChunk

class BaseRetriever(Protocol):
    def retrieve(self, query: str, k: int = 4) -> list[RetrievedChunk]:
        ...