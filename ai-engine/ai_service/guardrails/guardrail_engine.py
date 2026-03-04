# ai_service/guardrails/guardrail_engine.py

import os
from dotenv import load_dotenv

load_dotenv()


class GuardrailEngine:

    VERSION = os.getenv("AI_GUARDRAIL_VERSION", "1.0")

    def apply(self, decision: dict, ticket_text: str) -> tuple[dict, str | None]:
        """
        Apply deterministic safety rules on top of LLM decision.
        Returns modified decision and guardrail_triggered (if any).
        """

        # Rule 1 — High urgency must escalate
        if decision["urgency"] == "high" and decision["escalation_required"] is False:
            decision["escalation_required"] = True
            return decision, "GR-001: High urgency auto-escalation"

        # Rule 2 — Legal threat must escalate
        legal_keywords = ['legal', 'lawyer', 'attorney', 'lawsuit', 'sue', 'court', 'legal action', 'legal threat', 'legal notice']
        if any(keyword in ticket_text.lower() for keyword in legal_keywords) and decision["escalation_required"] is False:
            decision["escalation_required"] = True
            return decision, "GR-002: Legal threat auto-escalation"

        # Rule 3 — FAQ forbidden for high urgency
        if (
            decision["urgency"] == "high"
            and decision["recommended_policy"] == "faq_support_v1"
        ):
            decision["recommended_policy"] = "procedure_escalation_sav_v1"
            return decision, "GR-003: FAQ forbidden for high urgency"

        return decision, 'None'