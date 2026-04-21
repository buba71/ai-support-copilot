from pathlib import Path

from ai_service.infrastructure.doc_loader import load_docs
from ai_service.infrastructure.vector_db import VectorDB
from ai_service.rag.chunker import chunk_text

RAG_DOCS_DIR = Path(__file__).resolve().parent.parent / "rag_docs"


def build_indexable_documents(
    path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:
    raw_docs = load_docs(path)
    documents = []

    for raw_doc in raw_docs:
        source = raw_doc["source"]
        content = raw_doc["content"]

        chunks = chunk_text(
            content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        print(f"Document {source}: {len(chunks)} chunks")

        source_stem = Path(source).stem

        for index, chunk in enumerate(chunks):
            documents.append({
                "id": f"{source_stem}_chunk_{index}",
                "content": chunk,
                "metadata": {
                    "source": source,
                    "source_id": source_stem,
                    "type": "text_file",
                    "chunk_index": index,
                    "chunk_count": len(chunks),
                },
            })

    return documents


def main():
    db = VectorDB()
    docs = build_indexable_documents(str(RAG_DOCS_DIR))

    if not docs:
        print("⚠️ No documents found in rag_docs/")
        return

    indexed = 0
    skipped = 0

    for doc in docs:
        if db.exists(doc["id"]):
            skipped += 1
            continue

        db.index_documents([doc])
        indexed += 1

    print(f"✅ {indexed} chunks indexed")
    print(f"⏭️ {skipped} chunks skipped (already indexed)")


if __name__ == "__main__":
    main()