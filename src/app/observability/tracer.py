import time
import uuid


class QueryTrace:
    def __init__(self, query: str):
        self.id = str(uuid.uuid4())
        self.query = query
        self.start_time = time.time()

        self.stages = {
            "bm25": [],
            "dense": [],
            "fusion": [],
            "rerank": []
        }

        self.final = []

    def add_stage(self, name: str, data: list):
        if name in self.stages:
            self.stages[name] = data

    def set_final(self, data: list):
        self.final = data

    def to_dict(self):
        return {
            "id": self.id,
            "query": self.query,
            "latency_ms": round((time.time() - self.start_time) * 1000, 2),
            "stages": self.stages,
            "final": self.final
        }