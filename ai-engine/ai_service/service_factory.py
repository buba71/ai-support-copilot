from ai_service.infrastructure.llm_client import LLMClient
from ai_service.rag_service import RagService
from ai_service.monitoring.monitoring_service import MonitoringService
from ai_service.guardrails.guardrail_engine import GuardrailEngine
from ai_service.cache.llm_cache_service import LLMCacheService
from ai_service.retrieval.chroma_retriever import ChromaRetriever
from ai_service.infrastructure.vector_db import VectorDB
from ai_service.ticket_analyser import TicketAnalyzer

from ai_service.infrastructure.redis_connection import get_redis_connection

def get_ticket_analyzer() -> TicketAnalyzer:
    """
    Factory function to create a fully configured TicketAnalyzer instance.
    This centralizes dependency management and simplifies injection.
    """
    redis_conn = get_redis_connection()
    
    vector_db = VectorDB()
    retriever = ChromaRetriever(
        vector_db=vector_db,
        default_k=4,
        candidate_k=8,
        min_score=0.0
    )
    rag_service = RagService(retriever=retriever)

    return TicketAnalyzer(
        llm_client=LLMClient(),
        rag_service=rag_service,
        monitoring_service=MonitoringService(),
        guardrail_engine=GuardrailEngine(),
        cache_service=LLMCacheService(redis_client=redis_conn)
    )
