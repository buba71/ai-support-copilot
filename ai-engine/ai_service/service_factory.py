from ai_service.infrastructure.llm_client import LLMClient
from ai_service.rag_service import RagService
from ai_service.monitoring.monitoring_service import MonitoringService
from ai_service.guardrails.guardrail_engine import GuardrailEngine
from ai_service.cache.llm_cache_service import LLMCacheService
from ai_service.ticket_analyser import TicketAnalyzer

from ai_service.infrastructure.redis_connection import get_redis_connection

def get_ticket_analyzer() -> TicketAnalyzer:
    """
    Factory function to create a fully configured TicketAnalyzer instance.
    This centralizes dependency management and simplifies injection.
    """
    redis_conn = get_redis_connection()

    return TicketAnalyzer(
        llm_client=LLMClient(),
        rag_service=RagService(),
        monitoring_service=MonitoringService(),
        guardrail_engine=GuardrailEngine(),
        cache_service=LLMCacheService(redis_client=redis_conn)
    )
