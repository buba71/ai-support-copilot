from enum import Enum

class RetrievalProfile(str, Enum):
    FAQ = "faq"
    STANDARD = "standard"
    ADVANCED = "advanced"