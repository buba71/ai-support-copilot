from ai_service.core.schemas.retrieval import RetrievedChunk
from ai_service.infrastructure.vector_db import VectorDB
from ai_service.core.logging.config import get_logger

logger = get_logger(__name__)


class ChromaRetriever:
    """
    Chroma-based retriever implementation.
    """
    VERSION = "chroma_v1"

    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db

    def retrieve(self, query: str, k: int = 4) -> list[RetrievedChunk]:
        logger.info("[TECH] retrieve_start query=%s", query)
        candidates = self.vector_db.search(query, k=8)

        results: list[RetrievedChunk] = []
        for item in candidates:
            metadata = item.get("metadata", {})
            distance = item.get("distance")

            score = None
            if distance is not None:
                score = round(1 - distance, 3)

            results.append(
                RetrievedChunk(
                    content=item["content"],
                    source=metadata.get("source", "unknown"),
                    score=score,
                    metadata=metadata,
                )
            )

        results.sort(
            key=lambda chunk: chunk.score if chunk.score is not None else 0.0,
            reverse=True,
        )
        logger.info("[TECH] retrieve_end results=%s", len(results))
        return results[:k]