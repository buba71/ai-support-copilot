from pydantic import BaseModel, Field
from ai_service.core.schemas.reliable_ticket_analysis import ReliableTicketAnalysis

class SupportCopilotResponse(BaseModel):
    internal_analysis: ReliableTicketAnalysis = Field(
        ...,
        description="Internal support analysis used by the support agent"
    )

    draft_reply: str = Field(
        ...,
        description="Draft reply that can be sent to the customer"
    )
