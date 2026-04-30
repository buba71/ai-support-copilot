
class EvaluationMetrics:
    def __init__(self):
        self.total = 0
        self.category_correct = 0
        self.priority_correct = 0
        self.policy_correct = 0
        self.source_correct = 0
        self.escalation_correct = 0
        self.errors = 0

    def update(
        self,
        expected_category,
        expected_priority,
        expected_sources,
        expected_escalation,
        result
    ):

        self.total += 1

        if "error" in result:
            self.errors += 1
            return

        decision = result.get("decision", {})

        if decision.get("category") == expected_category:
            self.category_correct += 1

        if decision.get("urgency") == expected_priority:
            self.priority_correct += 1

        if decision.get("recommended_policy") in expected_sources:
            self.policy_correct += 1

        predicted_sources = [
            doc.get("source_id")
            for doc in decision.get("rag_documents", [])
            if doc.get("source_id")
        ]

        if any(source in predicted_sources for source in expected_sources):
            self.source_correct += 1

        if decision.get("escalation_required") == expected_escalation:
            self.escalation_correct += 1


    def summary(self):
        if self.total == 0:
            return {}

        return {
            "total": self.total,
            "category_accuracy": round(self.category_correct / self.total * 100, 2),
            "priority_accuracy": round(self.priority_correct / self.total * 100, 2),
            "source_accuracy": round(self.source_correct / self.total * 100, 2),
            "escalation_accuracy": round(self.escalation_correct / self.total * 100, 2),
            "error_rate": round(self.errors / self.total * 100, 2)
        }