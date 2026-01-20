from pathlib import Path
from ai_service.rag_service import RagService

def load_docs(path: str):
    docs = []
    for file in Path(path).glob("*.txt"):
        docs.append(file.read_text(encoding="utf-8"))
    return docs

documents = load_docs("rag_docs")
rag = RagService(documents) 