import json

from ai_service.core.schemas.retrieval import RetrievedChunk


class ContextComposer:
    def compose(
        self,
        rag_results: list[RetrievedChunk],
        tool_results: dict | None = None,
    ) -> str:
        sections = []

        if tool_results:
            sections.append(
                "=== TOOL CONTEXT ===\n"
                + json.dumps(tool_results, indent=2, ensure_ascii=False)
            )

        if rag_results:
            rag_context = "\n\n".join(
                doc.content for doc in rag_results
            )

            sections.append(
                "=== RAG CONTEXT ===\n" + rag_context
            )

        return "\n\n".join(sections)