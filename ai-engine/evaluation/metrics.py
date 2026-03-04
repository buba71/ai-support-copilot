
class EvaluationMetrics:
    def __init__(self):
        self.total = 0
        self.policy_correct = 0
        self.escalation_correct = 0
        self.errors = 0

    def update(self, expected_policy, expected_escalation, result):

        decision = result.get("decision", {})
        self.total += 1

        if "error" in result:
            self.errors += 1
            return

        if decision.get("recommended_policy") == expected_policy:
            self.policy_correct += 1

        if decision.get("escalation_required") == expected_escalation:
            self.escalation_correct += 1

    def summary(self):
        if self.total == 0:
            return {}

        return {
            "total": self.total,
            "policy_accuracy": round(self.policy_correct / self.total * 100, 2),
            "escalation_accuracy": round(self.escalation_correct / self.total * 100, 2),
            "error_rate": round(self.errors / self.total * 100, 2)
        }