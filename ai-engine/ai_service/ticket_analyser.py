import json
import time

from pydantic import ValidationError

from ai_service.llm_client import LLMClient
from ai_service.prompts import TICKET_ANALYSIS_PROMPT
from ai_service.models import TicketAnalysis
from ai_service.rag_service import RagService
from ai_service.monitoring import MonitoringService
from ai_service.guardrails import GuardrailEngine


class TicketAnalyzer:
    def __init__(self, rag_service: RagService):
        self.monitoring = MonitoringService()
        self.llm = LLMClient()
        self.rag = rag_service
        self.guardrail = GuardrailEngine()

    def analyze(self, ticket_text: str, use_rag: bool = True) -> dict:
        """
        Main orchestration method:
        - retrieve relevant knowledge (RAG)
        - build prompt
        - call LLM
        - validate response
        """

        if use_rag:
            # 1. Retrieve relevant documents from 
            rag_results = self.rag.search(ticket_text, k=4)
            context = "\n\n".join([doc["content"] for doc in rag_results])

        else:
            rag_results = []
            context = ""

        # 2. Build the final prompt

        prompt = TICKET_ANALYSIS_PROMPT.format(
            context=context,
            ticket=ticket_text
        )

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

        # 3. Call LLM

        start = time.time() # start time in seconds 
        llm_response = self.llm.ask(messages)
        latency_ms = int((time.time() - start) * 1000) # latency in milliseconds

        raw_response = llm_response["response"]
        tokens_input = llm_response["tokens_input"]
        tokens_output = llm_response["tokens_output"]

        # 4. Parse and validate response

        try:
            data = json.loads(raw_response)
            validated_data = TicketAnalysis(**data)

            decision = validated_data.dict()

            # 5. Apply safety guardrails (logic-based corrections)
            # Uses tuple unpacking (similar to list() in PHP) to get the updated decision and trigger status
            decision, guardrail_triggered = self.guardrail.apply(
                decision,
                ticket_text
            )

            decision["rag_documents"] = [
                {
                    "source": doc["source"],
                    "score": doc["score"],
                    "excerpt": doc["content"][:500]
                }
                for doc in rag_results
            ]

            result = self.monitoring.enrich(
                decision,
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                latency_ms=latency_ms,
                rag_enabled=use_rag,
                guardrail_triggered=guardrail_triggered, # for future use_rag
            )

            return result

        except json.JSONDecodeError:

            return {
                "error": "Invalid response from LLM client - response was not valid JSON",
                "raw_response": raw_response[:500]  # Limit length for logging
            }

        except ValidationError as e:
            return {
                "error": "INVALID_SCHEMA",
                "details": e.errors(),
                "raw_response": raw_response[:500] # Limit length for logging
            }
