from ai_service.core.schemas.ticket_classification import TicketClassification


class TicketClassifier:
    def classify(self, ticket_text: str) -> TicketClassification:
        lowered_text = ticket_text.lower()

        if "mot de passe" in lowered_text or "connexion" in lowered_text:
            return TicketClassification(
                category="faq_support",
                urgency="low",
                complexity="low"
            )

        if "retard" in lowered_text or "réparation" in lowered_text:
            return TicketClassification(
                category="repair_delay",
                urgency="medium",
                complexity="low"
            )

        if "premium" in lowered_text:
            return TicketClassification(
                category="premium_extension",
                urgency="medium",
                complexity="high"
            )

        if "cassé" in lowered_text or "mauvaise utilisation" in lowered_text:
            return TicketClassification(
                category="accidental_damage",
                urgency="medium",
                complexity="high"
            )

        if "litige" in lowered_text or "remboursement" in lowered_text:
            return TicketClassification(
                category="customer_dispute",
                urgency="high",
                complexity="high"
            )

        return TicketClassification(
            category="product_defect",
            urgency="medium",
            complexity="medium"
        )