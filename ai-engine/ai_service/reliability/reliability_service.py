from ai_service.core.schemas.retrieval import RetrievedChunk
from ai_service.core.logging.config import get_logger

logger = get_logger(__name__)


class ReliabilityService:

    def evaluate(
        self,
        retrieved_chunks: list[RetrievedChunk],
        guardrail_reason: str | None,
        request_id: str,
    ) -> dict:

        used_sources = list(dict.fromkeys(
            chunk.source
            for chunk in retrieved_chunks
            if chunk.source
        ))

        scores = [
            chunk.score
            for chunk in retrieved_chunks
            if chunk.score is not None
        ]

        best_score = max(scores) if scores else None

        if not used_sources or best_score is None or best_score < 0.45:

            logger.warning(
                "[%s][BUSINESS] insufficient_context_detected best_score=%s",
                request_id,
                best_score
            )

            logger.warning(
                "[%s][BUSINESS] confidence_score=0.35 insufficient_context=True",
                request_id
            )

            return {
                "confidence_score": 0.35,
                "used_sources": used_sources,
                "insufficient_context": True,
                "fallback_reason": "No sufficiently relevant source found",
            }

        confidence_score = 0.8
        fallback_reason = None

        if guardrail_reason:
            confidence_score = min(
                confidence_score,
                0.75
            )

            fallback_reason = guardrail_reason

        logger.info(
            "[%s][BUSINESS] confidence_score=%s insufficient_context=%s",
            request_id,
            confidence_score,
            False
        )

        return {
            "confidence_score": confidence_score,
            "used_sources": used_sources,
            "insufficient_context": False,
            "fallback_reason": fallback_reason,
        }