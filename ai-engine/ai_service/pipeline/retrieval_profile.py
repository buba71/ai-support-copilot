from enum import Enum
from pydantic import BaseModel

class RetrievalProfileName(str, Enum):
    FAQ = "faq"
    STANDARD = "standard"
    ADVANCED = "advanced"


class RetrievalProfile(BaseModel):
    name: RetrievalProfileName
    top_k: int