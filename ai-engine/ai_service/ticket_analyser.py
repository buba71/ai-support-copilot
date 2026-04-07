import json
import time

from pydantic import ValidationError

from ai_service.infrastructure.llm_client import LLMClient
from ai_service.prompts import TICKET_ANALYSIS_PROMPT
from ai_service.models import TicketAnalysis
from ai_service.rag_service import RagService
from ai_service.monitoring import MonitoringService
from ai_service.guardrails import GuardrailEngine
from ai_service.cache.llm_cache_service import LLMCacheService


class TicketAnalyzer:
    def __init__(
        self,
        llm_client: LLMClient,
        rag_service: RagService,
        monitoring_service: MonitoringService,
        guardrail_engine: GuardrailEngine,
        cache_service: LLMCacheService
    ):
        self.llm = llm_client
        self.rag = rag_service
        self.monitoring = monitoring_service
        self.guardrail = guardrail_engine
        self.cache = cache_service

    def analyze(self, ticket_text: str, use_rag: bool = True) -> dict:
        """
        Main orchestration method using specialized private methods.
        """
        # 1. Context Retrieval
        rag_results, context = self._get_context(ticket_text, use_rag)

        # 2. Prompt Building
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
            return self._format_cache_hit(cached_response)

        start = time.time()
        llm_response = self.llm.ask(messages)
        latency_ms = int((time.time() - start) * 1000)

        raw_response = llm_response["response"]
        tokens_input = llm_response["tokens_input"]
        tokens_output = llm_response["tokens_output"]

        # 4. Parse and Validate
        parsed_data, error_response = self._parse_and_validate(raw_response)
        if error_response:
            return error_response

        # 5. Post-process (Guardrails & RAG Docs)
        decision, guardrail_triggered = self._post_process(parsed_data, ticket_text, rag_results)

        # 6. Final Enrichment & Cache
        result = self.monitoring.enrich(
            decision,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            latency_ms=latency_ms,
            rag_enabled=use_rag,
            guardrail_triggered=guardrail_triggered,
            cache_hit=False
        )

        self.cache.set(prompt, result)
        return result

    def _get_context(self, ticket_text: str, use_rag: bool) -> tuple:
        if use_rag:
            rag_results = self.rag.search(ticket_text, k=4)
            context = "\n\n".join([doc["content"] for doc in rag_results])
            return rag_results, context
        return [], ""

    def _get_prompt(self, ticket_text: str, context: str) -> str:
        return TICKET_ANALYSIS_PROMPT.format(
            context=context,
            ticket=ticket_text
        )

    def _format_cache_hit(self, cached_response: dict) -> dict:
        result = cached_response.copy()
        result["meta"] = cached_response["meta"].copy()
        result["meta"].update({
            "cache_hit": True,
            "latency_ms": 0,
            "tokens_input": 0,
            "tokens_output": 0,
            "estimated_cost": 0.0
        })
        return result

    def _parse_and_validate(self, raw_response: str) -> tuple:
        try:
            data = json.loads(raw_response)
            validated_data = TicketAnalysis(**data)
            return validated_data.dict(), None
        except json.JSONDecodeError:
            return None, {
                "error": "Invalid response from LLM client - response was not valid JSON",
                "raw_response": raw_response[:500]
            }
        except ValidationError as e:
            return None, {
                "error": "INVALID_SCHEMA",
                "details": e.errors(),
                "raw_response": raw_response[:500]
            }

    def _post_process(self, decision: dict, ticket_text: str, rag_results: list) -> tuple:
        updated_decision, triggered = self.guardrail.apply(decision, ticket_text)
        
        updated_decision["rag_documents"] = [
            {
                "source": doc["source"],
                "score": doc["score"],
                "excerpt": doc["content"][:500]
            }
            for doc in rag_results
        ]
        return updated_decision, triggered
