from typing import Any
from pydantic import BaseModel, Field

class RetrievedChunk(BaseModel):
    """
    Represents a chunk of text retrieved from the knowledge base.
    """
    content: str
    source: str
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    