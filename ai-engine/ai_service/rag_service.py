from ai_service.core.schemas.retrieval import RetrievedChunk
from ai_service.retrieval.base import BaseRetriever

class RagService:
    def __init__(self, retriever: BaseRetriever):
        self.retriever = retriever

    def get_retriever_name(self) -> str:
        return getattr(self.retriever, "VERSION", "unknown")

    def search(self, query: str, k: int | None = None)->list[RetrievedChunk]:
        return self.retriever.retrieve(query, k=k)
