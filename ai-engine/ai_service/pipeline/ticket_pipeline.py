from ai_service.classification.ticket_classifier import TicketClassifier
from ai_service.pipeline.routing_service import RoutingService
from ai_service.ticket_analyser import TicketAnalyzer
from ai_service.tools.warranty_eligibility_tool import InMemoryWarrantyEligibilityTool


class TicketPipeline:
    def __init__(
        self,
        classifier: TicketClassifier,
        router: RoutingService,
        analyzer: TicketAnalyzer,
        warranty_tool: InMemoryWarrantyEligibilityTool
    ):
        self.classifier = classifier
        self.router = router
        self.analyzer = analyzer
        self.warranty_tool = warranty_tool

    def run(
        self,
        ticket_text: str,
        use_rag: bool = True,
        request_id: str | None = None,
    ) -> dict:

        tool_results = {}
        classification = self.classifier.classify(ticket_text)

        profile = self.router.select_profile(
            category=classification.category,
            complexity=classification.complexity,
        )

        if profile.name.value == "advanced":
            tool_results["warranty_eligibility"] = self.warranty_tool.execute(product_id="demo_product_id")

        result = self.analyzer.analyze(
            ticket_text=ticket_text,
            use_rag=use_rag,
            request_id=request_id,
            retrieval_k=profile.top_k,
            tool_results=tool_results
        )

        result["meta"]["pipeline"] = {
            "classification": classification.model_dump(),
            "retrieval_profile": profile.name.value,
            "retrieval_top_k": profile.top_k,
            "tools": tool_results
        }

        return result