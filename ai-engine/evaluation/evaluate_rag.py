import json
import argparse
from ai_service.service_factory import get_ticket_analyzer
from evaluation.metrics import EvaluationMetrics


def load_dataset(dataset_path: str):
    with open(dataset_path, "r") as f:
        return json.load(f)

def debug_examples(analyzer, dataset, use_rag: bool, limit: int = 5):
    print(f"\n=== DEBUG EXAMPLES | RAG={use_rag} ===")

    category_errors = []
    priority_errors = []
    escalation_errors = []

    for item in dataset:
        result = analyzer.analyze(item["ticket_input"], use_rag=use_rag)
        decision = result.get("decision", {})

        if decision.get("category") != item["expected_category"]:
            category_errors.append({
                "id": item["id"],
                "ticket": item["ticket_input"],
                "expected": item["expected_category"],
                "predicted": decision.get("category"),
                "policy": decision.get("recommended_policy"),
                "rag_sources": [
                    doc.get("source") for doc in decision.get("rag_documents", [])
                ],
            })

        if decision.get("urgency") != item["expected_priority"]:
            priority_errors.append({
                "id": item["id"],
                "expected": item["expected_priority"],
                "predicted": decision.get("urgency"),
                "category": decision.get("category"),
            })

        if decision.get("escalation_required") != item["expected_escalation"]:
            escalation_errors.append({
                "id": item["id"],
                "expected": item["expected_escalation"],
                "predicted": decision.get("escalation_required"),
                "category": decision.get("category"),
                "priority": decision.get("urgency"),
                "policy": decision.get("recommended_policy"),
            })

    print("\n=== CATEGORY ERRORS ===")
    for e in category_errors:
        print(e)

    print("\n=== PRIORITY ERRORS ===")
    for e in priority_errors:
        print(e)

    print("\n=== ESCALATION ERRORS ===")
    for e in escalation_errors:
        print(e)


def run_evaluation(dataset, use_rag: bool):
    analyzer = get_ticket_analyzer()

    debug_examples(analyzer, dataset, use_rag=use_rag, limit=5)

    metrics = EvaluationMetrics()

    for item in dataset:
        result = analyzer.analyze(item["ticket_input"], use_rag=use_rag)

        metrics.update(
            expected_category=item["expected_category"],
            expected_priority=item["expected_priority"],
            expected_sources=item["expected_sources"],
            expected_escalation=item["expected_escalation"],
            result=result
        )

    return metrics.summary()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)

    args = parser.parse_args()
    dataset = load_dataset(args.dataset)

    print("=== RAG ENABLED ===")
    rag_on = run_evaluation(dataset, use_rag=True)
    print(rag_on)

    print("\n=== RAG DISABLED ===")
    rag_off = run_evaluation(dataset, use_rag=False)
    print(rag_off)