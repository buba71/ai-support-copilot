"""
vector_db.py

Responsabilité unique :
- stocker des documents sous forme d'embeddings
- permettre une recherche sémantique

⚠️ Ce module :
- ne connaît PAS FastAPI
- ne connaît PAS le LLM
- ne connaît PAS le métier
"""

from typing import List, Dict
from dotenv import load_dotenv
import os

import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

class VectorDB:
    def __init__(
        self,
        collection_name: str = "support_docs",
        persist_directory: str = ".chroma"
    ):
        """
        Initialise (ou recharge) une base vectorielle locale Chroma.
        """
        self.persist_directory = persist_directory

        self.client = chromadb.PersistentClient(
            settings=chromadb.Settings(
                persist_directory=self.persist_directory
            )
        )

        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    # ------------------------------------------------------------
    # INGESTION
    # ------------------------------------------------------------
    def index_documents(self, documents: List[Dict]):
        """
        documents = [
            {
                "id": "policy_warranty_v1_1",
                "content": "text ...",
                "metadata": {"source": "policy_warranty_v1.txt"}
            }
        ]
        """
        ids = [doc["id"] for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]

        self.collection.add(
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )

        # self.client.persist()

    # ------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Recherche sémantique dans la base vectorielle.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        matches = []

        for i in range(len(results["documents"][0])):
            matches.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })

        return matches


# ------------------------------------------------------------
# TEST MANUEL (apprentissage)
# ------------------------------------------------------------
if __name__ == "__main__":
    """
    Test manuel isolé de la vector DB.
    À lancer depuis ai-engine :
        python -m ai_service.vector_db
    """

    db = VectorDB()

    sample_docs = [
        {
            "id": "warranty_1",
            "content": "A product under warranty can be replaced if defective.",
            "metadata": {"source": "policy_warranty_v1.txt"}
        },
        {
            "id": "escalation_1",
            "content": "A ticket must be escalated if the customer is premium.",
            "metadata": {"source": "procedure_escalation_sav_v1.txt"}
        }
    ]

    db.index_documents(sample_docs)

    results = db.search("defective product replacement")

    print("\n🔍 Résultats de recherche :\n")
    for r in results:
        print("-", r["metadata"]["source"], "→", r["content"])
