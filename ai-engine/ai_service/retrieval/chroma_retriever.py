from ai_service.core.schemas.retrieval import RetrievedChunk
from ai_service.infrastructure.vector_db import VectorDB
from ai_service.core.logging.config import get_logger
from ai_service.retrieval.reranker import BaseReranker

logger = get_logger(__name__)


class ChromaRetriever:
    """
    Chroma-based retriever implementation.
    """
    VERSION = "chroma_v1"

    def __init__(
        self, vector_db: VectorDB,
        default_k: int = 4,
        candidate_k: int = 8,
        min_score: float = 0.0,
        reranker: BaseReranker | None = None,
    ):
        self.vector_db = vector_db
        self.default_k = default_k
        self.reranker = reranker
        self.candidate_k = candidate_k
        self.min_score = min_score

    def retrieve(self, query: str, k: int | None = None) -> list[RetrievedChunk]:
        final_k = k if k is not None else self.default_k

        if final_k <= 0:
            logger.warning("[TECH] invalid_final_k=%s defaulting_to=%s", final_k, self.default_k)
            final_k = self.default_k

        if self.candidate_k <= 0:
            logger.warning("[TECH] invalid_candidate_k=%s defaulting_to=%s", self.candidate_k, self.default_k)

        logger.info(
            "[TECH] retrieval_start retriever=%s final_k=%s candidate_k=%s min_score=%s",
            self.VERSION,
            final_k,
            self.candidate_k,
            self.min_score,
        )

        candidates = self.vector_db.search(query, k=self.candidate_k)
        logger.info("[TECH] retrieval_candidates=%s", len(candidates))

        results: list[RetrievedChunk] = []
        for item in candidates:
            metadata = item.get("metadata", {})
            distance = item.get("distance")

            score = None
            if distance is not None:
                # Convert distance to a higher-is-better score for application-level ranking.
                # This is a local convention and depends on the underlying distance metric.
                score = round(1 - distance, 3)

            chunk = RetrievedChunk(
                content=item["content"],
                source=metadata.get("source", "unknown"),
                score=score,
                metadata=metadata,
            )

            if chunk.score is None or chunk.score >= self.min_score:
                results.append(chunk)

        results.sort(
            key=lambda chunk: chunk.score if chunk.score is not None else 0.0,
            reverse=True,
        )

        if self.reranker is not None:
            logger.info("[TECH] reranker_enabled")
            results = self.reranker.rerank(query, results)
        else:
            logger.info("[TECH] reranker_disabled")

        final_results = results[:final_k]

        logger.info(
            "[TECH] retrieval_filtered=%s retrieval_final=%s",
            len(results),
            len(final_results),
        )
        return final_results