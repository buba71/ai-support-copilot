from ai_service.infrastructure.vector_db import VectorDB

class RagService:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db

    def search(self, query: str, k: int = 2):
        """
        Returns enriched chunks:
        - content
        - source
        - score
        """
        candidates = self.vector_db.search(query, k=8)

        enriched_results = []
        for item in candidates:
            enriched_results.append({
                "content": item["content"],
                "source": item["metadata"].get("source"),
                "score": round(1 - item["distance"], 3) # score = 1 - distance (closer = higher score)
            })
        
        # Sort by score
        enriched_results.sort(key=lambda x: x["score"], reverse=True)

        # Take top k
        return enriched_results[:int(k)]

