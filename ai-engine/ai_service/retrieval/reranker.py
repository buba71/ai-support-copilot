from typing import Protocol

from ai_service.core.schemas.retrieval import RetrievedChunk


class BaseReranker(Protocol):
    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        ...