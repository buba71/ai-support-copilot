from typing import Optional
from pydantic import Field
from ai_service.core.schemas.ticket_analysis import TicketAnalysis

class ReliableTicketAnalysis(TicketAnalysis):
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )

    used_sources: list[str] = Field(
        default_factory=list,
        description="Knowledge base sources used for the analysis"
    )

    insufficient_context: bool = Field(
        default=False,
        description="Whever the retrieved context was insufficient"
    )

    fallback_reason: Optional[str] = Field(
        default=None,
        description="Reason explaining degraded or fallback behavior"
    )
