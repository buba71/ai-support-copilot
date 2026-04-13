from typing import Any
from pydantic import BaseModel, Field

class RetrievedChunk(BaseModel):
    content: str
    source: str
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    