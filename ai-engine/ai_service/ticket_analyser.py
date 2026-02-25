import json
from pydantic import ValidationError

from ai_service.llm_client import LLMClient
from ai_service.prompts import TICKET_ANALYSIS_PROMPT
from ai_service.models import TicketAnalysis
from ai_service.rag_service import RagService


class TicketAnalyzer:
    def __init__(self, rag_service: RagService):
        self.llm = LLMClient()
        self.rag = rag_service

    def analyze(self, ticket_text: str, rag_usage: bool = True) -> dict:
        """
        Main orchestration method:
        - retrieve relevant knowledge (RAG)
        - build prompt
        - call LLM
        - validate response
        """

        if  rag_usage:
            # 1. Retrieve relevant documents from 
            rag_results = self.rag.search(ticket_text, k=2)

            context = "\n\n".join([doc["content"] for doc in rag_results])
        else:
            rag_results = []
            context = ""

        # 2. Build the final prompt

        prompt = f"""
            {TICKET_ANALYSIS_PROMPT}

            Ticket:
            {ticket_text}

            Context:
            {context}
            """

        messages = [
            {
                "role": "system",
                "content": "You are a precise and reliable AI assistant for customer support decisions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # 3. Call LLM

        raw_response = self.llm.ask(messages)

        # 4. Parse and validate response

        try:
            data = json.loads(raw_response)
            validated_data = TicketAnalysis(**data)

            result = validated_data.dict()

            result["rag_documents"] = [
                {
                    "source": doc["source"],
                    "score": doc["score"],
                    "excerpt": doc["content"][:500]
                }
                for doc in rag_results
            ]

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
