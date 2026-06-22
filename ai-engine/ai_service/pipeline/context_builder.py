class ContextBuilder:

    def build(
        self,
        rag_context: str,
        tool_context: dict | None,
    ) -> str:

        parts = []

        if tool_context:
            parts.append(
                f"TOOL_CONTEXT:\n{tool_context}"
            )

        if rag_context:
            parts.append(
                f"RAG_CONTEXT:\n{rag_context}"
            )

        return "\n\n".join(parts)