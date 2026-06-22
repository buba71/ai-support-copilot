import json
import time
import uuid

from pydantic import ValidationError

from ai_service.prompts import TICKET_ANALYSIS_PROMPT
from ai_service.monitoring import MonitoringService
from ai_service.guardrails import GuardrailEngine
from ai_service.cache.llm_cache_service import LLMCacheService
from ai_service.core.logging.config import get_logger
from ai_service.core.interfaces.llm_client_interface import LLMClientInterface
from ai_service.core.interfaces.rag_service_interface import RagServiceInterface
from ai_service.core.schemas.reliable_ticket_analysis import ReliableTicketAnalysis
from ai_service.core.schemas.retrieval import RetrievedChunk
from ai_service.core.schemas.support_copilot_response import SupportCopilotResponse
from ai_service.core.schemas.ticket_analysis import TicketAnalysis
from ai_service.post_processing.decision_normalizer import DecisionNormalizer
from ai_service.classification.ticket_classifier import TicketClassifier

logger = get_logger(__name__)


class TicketAnalyzer:
    def __init__(
        self,
        llm_client: LLMClientInterface,
        rag_service: RagServiceInterface,
        monitoring_service: MonitoringService,
        guardrail_engine: GuardrailEngine,
        cache_service: LLMCacheService,
        normalizer: DecisionNormalizer,
        classifier: TicketClassifier
    ):
        self.llm = llm_client
        self.rag = rag_service
        self.monitoring = monitoring_service
        self.guardrail = guardrail_engine
        self.cache = cache_service
        self.normalizer = normalizer
        self.classifier = classifier

    def analyze(self, ticket_text: str, use_rag: bool = True, request_id: str | None = None) -> dict:
        """
        Main orchestration method using specialized private methods.
        """
        total_start = time.time()   
        
        # Generate request_id if not provided
        if request_id is None:
            request_id = f"req_{uuid.uuid4().hex[:8]}"

        logger.info("[%s][TECH] analyze_start use_rag=%s", request_id, use_rag)

        classification = self.classifier.classify(ticket_text)

        logger.info(
            "[%s][BUSINESS] classification | category=%s | urgency=%s | complexity=%s",
            request_id,
            classification.category,
            classification.urgency,
            classification.complexity
        )

        retrieval_start = time.time()
        rag_results, context = self._get_context(ticket_text, use_rag, request_id)
        retrieval_latency_ms = int((time.time() - retrieval_start) * 1000)

        logger.info(
            "[%s][TECH] retrieval_end latency_ms=%s",
            request_id,
            retrieval_latency_ms
        )

        prompt = self._get_prompt(ticket_text, context)
        messages = [
            {
                "role": "system",
                "content": "You are a strict AI that must always return valid JSON and nothing else."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # 3. Call LLM (with cache check)
        cached_response = self.cache.get(prompt)
        if cached_response is not None:
            return self._format_cache_hit(cached_response, request_id)

        llm_start = time.time()
        logger.info("[%s][TECH] cache_miss", request_id)
        logger.info("[%s][TECH] llm_call_start", request_id)
        llm_response = self.llm.ask(messages)
        raw_response = llm_response.response
        tokens_input = llm_response.tokens_input
        tokens_output = llm_response.tokens_output

        llm_latency_ms = int((time.time() - llm_start) * 1000)

        logger.info(
            "[%s][TECH] llm_call_end latency_ms=%s tokens_input=%s tokens_output=%s",
            request_id,
            llm_latency_ms,
            tokens_input,
            tokens_output
        )

        # 4. Parse and Validate
        post_processing_start = time.time()

        parsed_data, error_response = self._parse_and_validate(raw_response, request_id)
        if error_response:
            return error_response

        # 5. Normalize decision before guardrails
        logger.info("[%s][TECH] normalizing_decision", request_id)
        normalized_decision = self.normalizer.normalize(ticket_text, parsed_data)

        logger.info(
            "[%s][BUSINESS] normalized_decision category=%s priority=%s",
            request_id,
            normalized_decision["category"],
            normalized_decision["urgency"]
        )

        # 6. Apply guardrails and attach RAG docs
        decision, guardrail_triggered = self._post_process(
            normalized_decision,
            ticket_text,
            rag_results,
            request_id
        )

        logger.info(
            "[%s][BUSINESS] final_decision category=%s priority=%s guardrail_triggered=%s",
            request_id,
            decision["category"],
            decision["urgency"],
            guardrail_triggered
        )  

        guardrail_reason = "Guardrail triggered" if guardrail_triggered else None

        reliability_fields = self._build_reliability_fields(
            retrieved_chunks=rag_results,
            guardrail_reason=guardrail_reason,
            request_id=request_id
        ) 

        rag_documents = decision.get("rag_documents", [])

        decision_without_rag_documents = {
            key: value
            for key, value in decision.items()
            if key != "rag_documents"
        }

        reliable_decision = {
            **decision_without_rag_documents,
            **reliability_fields
        }

        reliable_decision = ReliableTicketAnalysis(
            **reliable_decision
        ).model_dump()

        reliable_decision["rag_documents"] = rag_documents

        draft_reply = self._build_draft_reply(reliable_decision)
        
        logger.info(
            "[%s][BUSINESS] draft_reply_generated",
            request_id
        )

        copilot_response = SupportCopilotResponse(
            internal_analysis=reliable_decision,
            draft_reply=draft_reply
        ).model_dump()

        post_processing_latency_ms = int(
            (time.time() - post_processing_start) * 1000
        )

        logger.info(
           "[%s][TECH] post_processing_end latency_ms=%s",
           request_id,
           post_processing_latency_ms
        )

        total_latency_ms = int(
            (time.time() - total_start) * 1000
        )

        logger.info(
           "[%s][TECH] total_end latency_ms=%s",
           request_id,
           total_latency_ms
        )

        # 7. Final Enrichment & Cache
        result = self.monitoring.enrich(
            copilot_response,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            rag_enabled=use_rag,
            guardrail_triggered=guardrail_triggered,
            cache_hit=False,
            retriever_name=self.rag.get_retriever_name(),
            request_id=request_id,
            retrieval_latency_ms=retrieval_latency_ms,
            llm_latency_ms=llm_latency_ms,
            post_processing_latency_ms=post_processing_latency_ms,
            total_latency_ms=total_latency_ms,
            latency_ms=total_latency_ms, # legacy field kept for backward compatibility
        )

        self.cache.set(prompt, result)

        return result

    def _get_context(self, ticket_text: str, use_rag: bool, request_id: str | None = None) -> tuple[list[RetrievedChunk], str]:
        if use_rag:
            rag_results = self.rag.search(ticket_text, k=4, request_id=request_id)
            context = "\n\n".join(doc.content for doc in rag_results)
            return rag_results, context
        return [], ""

    def _get_prompt(self, ticket_text: str, context: str) -> str:
        return TICKET_ANALYSIS_PROMPT.format(
            context=context,
            ticket=ticket_text
        )

    def _format_cache_hit(self, cached_response: dict, request_id: str | None = None) -> dict:
        logger.info(
            "[%s][TECH] cache_hit",
            request_id
        )

        result = cached_response.copy()
        result["meta"] = cached_response["meta"].copy()
        result["meta"].update({
            "request_id": request_id,
            "cache_hit": True,
            "retrieval_latency_ms": 0,
            "llm_latency_ms": 0,
            "post_processing_latency_ms": 0,
            "total_latency_ms": 0,
            "latency_ms": 0,
            "tokens_input": 0,
            "tokens_output": 0,
            "estimated_cost": 0.0
        })
        return result

    def _parse_and_validate(self, raw_response: str, request_id: str) -> tuple[dict | None, dict | None]:
        try:
            data = json.loads(raw_response)
            validated_data = TicketAnalysis(**data)
            return validated_data.model_dump(), None
        except json.JSONDecodeError:
            logger.error("[%s][TECH] invalid_json_from_llm", request_id)
            return None, {
                "error": "Invalid response from LLM client - response was not valid JSON",
                "raw_response": raw_response[:500]
            }
        except ValidationError as e:
            logger.error("[%s][TECH] invalid_schema_from_llm", request_id)
            return None, {
                "error": "INVALID_SCHEMA",
                "details": e.errors(),
                "raw_response": raw_response[:500]
            }

    def _post_process(self, decision: dict, ticket_text: str, rag_results: list, request_id: str) -> tuple[dict, bool]:
        updated_decision, triggered = self.guardrail.apply(decision, ticket_text)
        logger.info("[%s][BUSINESS] guardrail_triggered=%s", request_id, triggered)

        updated_decision["rag_documents"] = [
            {
                "source": doc.source,
                "source_id": doc.metadata.get("source_id"),
                "score": doc.score,
                "excerpt": doc.content[:500]
            }
            for doc in rag_results
        ]
        return updated_decision, triggered

    def _build_reliability_fields(
        self,
        retrieved_chunks: list[RetrievedChunk],
        guardrail_reason: str | None,
        request_id: str
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
                request_id, best_score
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
            request_id, confidence_score, False
        )
        
        return {
            "confidence_score": confidence_score,
            "used_sources": used_sources,
            "insufficient_context": False,
            "fallback_reason": fallback_reason
        }

    def _build_draft_reply(self, analysis: dict) -> str:
        if analysis.get("insufficient_context"):
            return (
                "Bonjour,\n\n"
                "Merci pour votre message. "
                "Nous avons bien reçu votre demande, mais les informations disponibles "
                "ne permettent pas encore d’apporter une réponse définitive. "
                "Votre dossier va être vérifié par un conseiller afin de vous apporter "
                "une réponse adaptée.\n\n"
                "Cordialement,\n"
                "Le service client"
            )

        if analysis.get("escalation_required"):
            return (
                "Bonjour,\n\n"
                "Merci pour votre message. "
                "Votre demande nécessite une vérification approfondie par notre équipe support. "
                "Nous allons transmettre votre dossier à un conseiller spécialisé afin de vous "
                "apporter une réponse adaptée.\n\n"
                "Cordialement,\n"
                "Le service client"
            )

        return (
            "Bonjour,\n\n"
            "Merci pour votre message. "
            "Après analyse de votre demande, notre équipe a identifié la procédure applicable. "
            "Nous allons traiter votre dossier conformément à notre politique support.\n\n"
            "Cordialement,\n"
            "Le service client"
        )
