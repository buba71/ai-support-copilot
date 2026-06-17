from typing import Literal
from pydantic import BaseModel, Field

class TicketClassification(BaseModel):
    category: Literal[
        "warranty",
        "premium_extension",
        "escalation",
        "repair_delay",
        "faq_support",
        "missing_item",
        "accidental_damage",
        "product_defect",
        "customer_dispute",
    ] = Field(
        ...,
        description="Initial category used to route the analysis pipeline"
    )

    urgency: Literal["low", "medium", "high"] = Field(
        ...,
        description="Initial urgency level"
    )

    complexity: Literal["low", "medium", "high"] = Field(
        ...,
        description="Estimated handling complexity"
    )
