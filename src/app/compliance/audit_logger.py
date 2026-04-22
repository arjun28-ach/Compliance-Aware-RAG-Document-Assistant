import json
from datetime import datetime
from pathlib import Path


class AuditLogger:
    def __init__(self, log_file: str = "app/logs/audit.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type: str, payload: dict):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "payload": payload,
        }
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")