from typing import Protocol
from ai_service.core.schemas.retrieval import RetrievedChunk


class RagServiceInterface(Protocol):
    def search(self, query: str, k: int = 2) -> list[RetrievedChunk]:
        ...    
    def get_retriever_name(self) -> str:
        ...