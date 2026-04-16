from typing import Protocol

from ai_service.core.schemas.retrieval import RetrievedChunk


class BaseRetriever(Protocol):
    VERSION: str

    def retrieve(self, query: str, k: int | None = None) -> list[RetrievedChunk]:
        ...