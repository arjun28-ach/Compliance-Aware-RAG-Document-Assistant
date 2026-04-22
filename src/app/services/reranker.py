from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self):
        # Lightweight but powerful model
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(self, query: str, documents: list[dict], top_k: int = 5):
        """
        documents: list of {"text": ..., "score": ..., "source": ...}
        """

        if not documents:
            return documents

        # 1. Prepare input pairs
        pairs = [(query, doc["text"]) for doc in documents]

        # 2. Get scores
        scores = self.model.predict(pairs)

        # 3. Attach scores
        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)

        # 4. Sort by rerank score
        documents = sorted(
            documents,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return documents[:top_k]