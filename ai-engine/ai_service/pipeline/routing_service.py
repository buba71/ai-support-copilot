from ai_service.pipeline.retrieval_profile import RetrievalProfile

class RoutingService:

    def select_profile(
        self,
        category: str,
        complexity: str,
    ) -> RetrievalProfile:

        if category == "faq_support":
            return RetrievalProfile.FAQ

        if complexity == "high":
            return RetrievalProfile.ADVANCED

        return RetrievalProfile.STANDARD