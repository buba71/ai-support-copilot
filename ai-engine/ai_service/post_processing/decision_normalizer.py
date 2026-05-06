class DecisionNormalizer:
    def __init__(self):
        pass

    def normalize(self, ticket_input: str, decision: dict) -> dict:
        decision = dict(decision)
        text = ticket_input.lower()

        decision = self._normalize_security(text, decision)
        decision = self._normalize_billing(text, decision)
        decision = self._normalize_refund(text, decision)

        return decision

    def _normalize_security(self, text: str, decision: dict) -> dict:
        if any(x in text for x in [
            "suspicious email", "password", "accessed my account",
            "without my consent", "outside your portal"
        ]):
            decision["category"] = "security_alert"
            decision["urgency"] = "high"
            decision["recommended_policy"] = "procedure_security_alerts_v1"
            decision["escalation_required"] = True
        return decision

    def _normalize_billing(self, text: str, decision: dict) -> dict:
        if any(x in text for x in [
            "invoice", "charged twice", "late fees", "tax amount"
        ]):
            if decision.get("category") == "customer_dispute":
                decision["category"] = "billing_dispute"
                decision["recommended_policy"] = "policy_billing_dispute_v1"
                decision["escalation_required"] = False
        return decision

    def _normalize_refund(self, text: str, decision: dict) -> dict:
        if any(x in text for x in ["refund", "return it", "changed my mind"]):
            decision["category"] = "refund_request"
            decision["recommended_policy"] = "policy_refund_policy_v1"
            decision["escalation_required"] = False
        return decision