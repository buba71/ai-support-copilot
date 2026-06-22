from ai_service.classification.ticket_classifier import TicketClassifier
from ai_service.ticket_analyser import TicketAnalyzer


class TicketPipeline:
    def __init__(
        self,
        classifier: TicketClassifier,
        analyzer: TicketAnalyzer,
    ):
        self.classifier = classifier
        self.analyzer = analyzer

    def run(
        self,
        ticket_text: str,
        use_rag: bool = True,
        request_id: str | None = None,
    ) -> dict:
        classification = self.classifier.classify(ticket_text)

        result = self.analyzer.analyze(
            ticket_text=ticket_text,
            use_rag=use_rag,
            request_id=request_id,
        )

        result["meta"]["classification"] = classification.model_dump()

        return result