import json
import os
from datetime import datetime


class QueryLogger:
    def __init__(self, log_file="app/logs/queries.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log(self, data: dict):
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(data) + "\n")
        except Exception:
            pass

    def log_query(self, query, results, latency, metadata=None):
        log_entry = {
            "type": "query",
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "latency_ms": round(latency * 1000, 2),
            "num_results": len(results),
            "results": results[:5],
            "metadata": metadata or {}
        }
        self.log(log_entry)

    # ✅ ADD THIS
    def log_trace(self, trace: dict):
        log_entry = {
            "type": "trace",
            "timestamp": datetime.utcnow().isoformat(),
            **trace
        }
        self.log(log_entry)