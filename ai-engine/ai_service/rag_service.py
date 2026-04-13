from ai_service.core.schemas.retrieval import RetrievedChunk
from ai_service.infrastructure.vector_db import VectorDB

class RagService:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db

    def search(self, query: str, k: int = 2)->list[RetrievedChunk]:

        candidates = self.vector_db.search(query, k=8)

        enriched_results: list[RetrievedChunk] = [] # Typed list of RetrievedChunk objects: variable name + : + type
        for item in candidates:
            enriched_results.append(
                RetrievedChunk(
                    content=item["content"],
                    source=item["metadata"].get("source", "Unknown"),
                    score=round(1 - item["distance"], 3), # score = 1 - distance (closer = higher score)
                    metadata=item.get("metadata", {})
                )
            )
        
        # Sort by score
        enriched_results.sort(key=lambda x: x["score"] if x["score"] is not None else 0.0, reverse=True)

        # Take top k
        return enriched_results[:int(k)]

