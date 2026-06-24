from ai_service.pipeline.retrieval_profile import RetrievalProfile, RetrievalProfileName

class RoutingService:
    def select_profile(
        self,
        category: str,
        complexity: str,
    ) -> RetrievalProfile:

        if category == "faq_support":
            return RetrievalProfile(
                name=RetrievalProfileName.FAQ,
                top_k=2,
            )

        if complexity == "high":
            return RetrievalProfile(
                name=RetrievalProfileName.ADVANCED,
                top_k=6,
            )

        return RetrievalProfile(
            name=RetrievalProfileName.STANDARD,
            top_k=4,
        )