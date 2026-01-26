import os
from pathlib import Path

from ai_service.vector_db import VectorDB

RAG_DOCS_DIR = Path(__file__).resolve().parent.parent / "rag_docs"


def load_documents():
    documents = []

    for file_path in RAG_DOCS_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "id": file_path.stem,
            "content": content,
            "metadata": {
                "source": file_path.name
            }
        })

    return documents


if __name__ == "__main__":

    db = VectorDB()
    docs = load_documents()

    if not docs:
        print("⚠️ No documents found in rag_docs/")
        exit(0)

    indexed = 0
    skipped = 0

    for doc in docs:
        if db.exists(doc["id"]):
            skipped += 1
            continue

        db.index_documents([doc])
        indexed += 1

    print(f"✅ {indexed} documents indexed")
    print(f"⏭️ {skipped} documents skipped (already indexed)")
