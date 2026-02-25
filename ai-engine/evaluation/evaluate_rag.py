import json
from ai_service.rag_service import RagService
from ai_service.ticket_analyser import TicketAnalyzer
from evaluation.metrics import EvaluationMetrics


def load_dataset():
    with open("evaluation/dataset.json", "r") as f:
        return json.load(f)


def run_evaluation(use_rag: bool):
    rag_service = RagService()
    analyzer = TicketAnalyzer(rag_service)
    dataset = load_dataset()

    metrics = EvaluationMetrics()

    for item in dataset:
        result = analyzer.analyze(item["ticket"], use_rag=use_rag)

        metrics.update(
            expected_policy=item["expected_policy"],
            expected_escalation=item["expected_escalation"],
            result=result
        )

    return metrics.summary()


if __name__ == "__main__":

    print("=== RAG ENABLED ===")
    rag_on = run_evaluation(use_rag=True)
    print(rag_on)

    print("\n=== RAG DISABLED ===")
    rag_off = run_evaluation(use_rag=False)
    print(rag_off)