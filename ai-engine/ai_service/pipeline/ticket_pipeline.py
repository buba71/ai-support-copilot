from ai_service.classification.ticket_classifier import TicketClassifier
from ai_service.pipeline.routing_service import RoutingService
from ai_service.pipeline.retrieval_profile import RetrievalProfile
from ai_service.ticket_analyser import TicketAnalyzer


class TicketPipeline:
    def __init__(
        self,
        classifier: TicketClassifier,
        router: RoutingService,
        analyzer: TicketAnalyzer,
    ):
        self.classifier = classifier
        self.router = router
        self.analyzer = analyzer

    def run(
        self,
        ticket_text: str,
        use_rag: bool = True,
        request_id: str | None = None,
    ) -> dict:
        classification = self.classifier.classify(ticket_text)

        profile = self.router.select_profile(
            category=classification.category,
            complexity=classification.complexity,
        )

        result = self.analyzer.analyze(
            ticket_text=ticket_text,
            use_rag=use_rag,
            request_id=request_id,
        )

        result["meta"]["pipeline"] = {
            "classification": classification.model_dump(),
            "retrieval_profile": profile.value,
        }

        return result