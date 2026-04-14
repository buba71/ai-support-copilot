import os

PROMPT_VERSION = os.getenv("AI_PROMPT_VERSION", "unknown")
MODEL_NAME = os.getenv("AI_MODEL_NAME", "unknown")
GUARDRAIL_VERSION = os.getenv("AI_GUARDRAIL_VERSION", "unknown")
MONITORING_VERSION = os.getenv("AI_MONITORING_VERSION", "unknown")
RETRIEVER_VERSION = os.getenv("AI_RETRIEVER_VERSION", "unknown")

# IMPORTANT → code-level version
SCHEMA_VERSION = "v1"