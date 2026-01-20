from pydantic import BaseModel, Field
from typing import Literal

class TicketAnalysis(BaseModel):
    summary: str = Field(..., description="A short summary of the ticket")
    category: str = Field(..., description="Issue category")
    urgency: Literal["low", "medium", "high"]