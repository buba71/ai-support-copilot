from pydantic import BaseModel, Field
from typing import Literal


class TicketAnalysis(BaseModel):
    summary: str = Field(
        ...,
        description="Short summary of the ticket"
    )

    category: str = Field(
        ...,
        description="Issue category"
    )

    urgency: Literal["low", "medium", "high"] = Field(
        ...,
        description="Urgency level"
    )

    recommended_policy: Literal[
        "policy_warranty_v1",
        "policy_premium_extension_v1",
        "procedure_escalation_sav_v1",
        "faq_support_v1"
    ] = Field(
        ...,
        description="Exact name of the applied policy document"
    )

    escalation_required: bool = Field(
        ...,
        description="Whether the case must be escalated to a senior agent"
    )

    justification: str = Field(
        ...,
        description="Short reasoning referencing the applied policy"
    )