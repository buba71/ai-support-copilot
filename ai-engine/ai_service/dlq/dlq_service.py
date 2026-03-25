import json
from datetime import datetime, UTC
from pathlib import Path


class DLQService:
    def __init__(self, filepath: str = "dlq/failed_jobs.jsonl"):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def store(
        self,
        *,
        ticket: str,
        error_type: str,
        error_message: str,
        attempts: int,
        retryable: bool,
        context: dict | None = None,
    ) -> None:
        payload = {
            "ticket": ticket,
            "error_type": error_type,
            "error_message": error_message,
            "attempts": attempts,
            "retryable": retryable,
            "timestamp": datetime.now(UTC).isoformat(),
            "context": context or {},
        }

        try:
            with self.filepath.open("a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception as e:
            print("DLQ write failed:", e) 