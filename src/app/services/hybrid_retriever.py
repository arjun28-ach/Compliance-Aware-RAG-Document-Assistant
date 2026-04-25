from app.observability.tracer import QueryTrace
from app.observability.logger import QueryLogger


class HybridRetriever:
    def __init__(self, vector_store, embedder, bm25_builder, reranker=None):
        self.store = vector_store
        self.embedder = embedder
        self.bm25_builder = bm25_builder
        self.reranker = reranker
        self.logger = QueryLogger()

        self.bm25 = None
        self.documents = []

        self.rerank_threshold = -2.0

    def initialize(self, documents=None):
        """
        No global initialization for document-isolated retrieval.

        Each uploaded PDF has its own doc_id. BM25 is built per document
        inside search() using get_documents_by_doc_id(doc_id).
        """
        self.documents = []
        self.bm25 = None

    def search(self, query: str, top_k: int = 5, doc_id: str | None = None, alpha: float = 0.5):
        if not query or not isinstance(query, str):
            return []

        alpha = max(0.0, min(1.0, alpha))

        # Get only this document's text for BM25
        bm25_results = []
        if doc_id:
            docs = self.store.get_documents_by_doc_id(doc_id)
        else:
            docs = self.documents

        if docs:
            try:
                temp_bm25 = self.bm25_builder.build(docs)
                bm25_results = temp_bm25.search(query, top_k=top_k * 3)
            except Exception:
                bm25_results = []

        dense_results = self.store.search_dense(
            query=query,
            embedder=self.embedder,
            top_k=top_k * 3,
            doc_id=doc_id,
        )

        bm25_results = self._normalize_bm25(bm25_results)

        combined = {}

        for text, score in bm25_results:
            combined[text] = {
                "text": text,
                "bm25": float(score),
                "dense": 0.0,
                "source": "Uploaded PDF",
                "doc_id": doc_id,
            }

        for r in dense_results:
            text = r.get("text")
            if not text:
                continue

            if text not in combined:
                combined[text] = {
                    "text": text,
                    "bm25": 0.0,
                    "dense": float(r.get("score", 0.0)),
                    "source": r.get("source", "Uploaded PDF"),
                    "doc_id": r.get("doc_id"),
                }
            else:
                combined[text]["dense"] = float(r.get("score", 0.0))
                combined[text]["source"] = r.get("source", "Uploaded PDF")
                combined[text]["doc_id"] = r.get("doc_id")

        fused = []

        for item in combined.values():
            score = alpha * item["dense"] + (1 - alpha) * item["bm25"]
            fused.append(
                {
                    "text": item["text"],
                    "score": float(score),
                    "source": item["source"],
                    "doc_id": item["doc_id"],
                }
            )

        fused.sort(key=lambda x: x["score"], reverse=True)

        if self.reranker and fused:
            try:
                return self.reranker.rerank(query, fused, top_k)
            except Exception:
                return fused[:top_k]

        return fused[:top_k]

    def _filter_reranked(self, results):
        filtered = []

        for item in results:
            rerank_score = item.get("rerank_score")
            if rerank_score is None:
                filtered.append(item)
                continue

            if rerank_score >= self.rerank_threshold:
                filtered.append(item)

        return filtered or results[:2]

    def _normalize_bm25(self, results):
        if not results:
            return []

        scores = [score for _, score in results]
        min_s, max_s = min(scores), max(scores)

        if max_s == min_s:
            return [(t, 1.0) for t, _ in results]

        return [
            (t, (s - min_s) / (max_s - min_s))
            for t, s in results
        ]