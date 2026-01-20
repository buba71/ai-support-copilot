import os
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RagService:
    def __init__(self, documents: list[str]):
        self.documents = documents
        self.embeddings = self._embed_documents(documents)

    def _embed_documents(self, docs):
        response = client.embeddings.create(
          model="text-embedding-3-small",
          input=docs
        )
        return [np.array(d.embedding) for d in response.data]

    def _embed_query(self, query: str):
        response = client.embeddings.create(
          model="text-embedding-3-small",
          input=[query]
        )
        return np.array(response.data[0].embedding)

    def _similarity(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def search(self, query: str, k=2):
        query_vec = self._embed_query(query)
        print(query_vec)

        results = []

        for doc, doc_vec in zip(self.documents, self.embeddings):
            score = self._similarity(query_vec, doc_vec)
            results.append((doc, score))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:k]