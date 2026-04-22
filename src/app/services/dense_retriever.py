from app.services.vector_store import VectorStore
from app.services.embedder import Embedder


class DenseRetriever:
    def __init__(self):
        self.store = VectorStore()
        self.embedder = Embedder()

    def search(self, query: str, top_k: int = 5):
        # 1. Convert query → vector
        query_vector = self.embedder.embed([query])[0]

        # 2. Query Qdrant
        results = self.store.client.query_points(
            collection_name=self.store.collection_name,
            query=query_vector,
            limit=top_k,
        )

        # 3. Format results
        formatted_results = []

        for r in results.points:
            formatted_results.append({
                "text": r.payload.get("text"),
                "source": r.payload.get("source"),
                "score": r.score
            })

        # ✅ 4. Normalize scores HERE (correct place)
        formatted_results = self.normalize_scores(formatted_results)

        return formatted_results

    def normalize_scores(self, results):
        if not results:
            return results

        scores = [r["score"] for r in results]
        min_score = min(scores)
        max_score = max(scores)

        for r in results:
            if max_score - min_score == 0:
                r["score"] = 1.0
            else:
                r["score"] = (r["score"] - min_score) / (max_score - min_score)

        return results