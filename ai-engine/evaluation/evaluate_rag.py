import json
from ai_service.service_factory import get_ticket_analyzer
from evaluation.metrics import EvaluationMetrics


def load_dataset():
    with open("evaluation/dataset.json", "r") as f:
        return json.load(f)

def debug_examples(analyzer, dataset, use_rag: bool, limit: int = 5):
    print(f"\n=== DEBUG EXAMPLES | RAG={use_rag} ===")

    for item in dataset[:limit]:
        result = analyzer.analyze(item["ticket_input"], use_rag=use_rag)
        decision = result.get("decision", {})

        print("ID:", item["id"])
        print("TICKET:", item["ticket_input"])

        print("EXPECTED CATEGORY:", item["expected_category"])
        print("PREDICTED CATEGORY:", decision.get("category"))

        print("EXPECTED PRIORITY:", item["expected_priority"])
        print("PREDICTED URGENCY:", decision.get("urgency"))

        print("EXPECTED SOURCES:", item["expected_sources"])
        print("PREDICTED POLICY:", decision.get("recommended_policy"))

        print("RAG SOURCES:", [
            doc.get("source") for doc in decision.get("rag_documents", [])
        ])

        print("EXPECTED ESCALATION:", item["expected_escalation"])
        print("PREDICTED ESCALATION:", decision.get("escalation_required"))

        print("-" * 60)

        if decision.get("category") != item["expected_category"]:
            print("CATEGORY ERROR")
            print("ID:", item["id"])
            print("EXPECTED:", item["expected_category"])
            print("PREDICTED:", decision.get("category"))
            print("POLICY:", decision.get("recommended_policy"))
            print("ESCALATION:", decision.get("escalation_required"))
            print("-" * 60)

        if decision.get("escalation_required") != item["expected_escalation"]:
            print("ESCALATION ERROR")
            print("ID:", item["id"])
            print("EXPECTED:", item["expected_escalation"])
            print("PREDICTED:", decision.get("escalation_required"))
            print("CATEGORY:", decision.get("category"))
            print("URGENCY:", decision.get("urgency"))
            print("POLICY:", decision.get("recommended_policy"))
            print("-" * 60)


def run_evaluation(use_rag: bool):
    analyzer = get_ticket_analyzer()
    dataset = load_dataset()

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

    print("=== RAG ENABLED ===")
    rag_on = run_evaluation(use_rag=True)
    print(rag_on)

    print("\n=== RAG DISABLED ===")
    rag_off = run_evaluation(use_rag=False)
    print(rag_off)