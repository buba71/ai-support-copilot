from pathlib import Path
from typing import List, Dict, Any

def load_docs(path: str)->List[Dict[str, Any]]:
    docs = []

    for file in Path(path).glob("*.txt"):

        docs.append({
            "source": file.name,
            "content": file.read_text(encoding="utf-8")
        })

    return docs