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
        docs = documents or self.store.get_all_documents() or []

        if not docs:
            self.documents = []
            self.bm25 = None
            return

        self.documents = docs
        self.bm25 = self.bm25_builder.build(docs)

    def search(self, query: str, top_k: int = 5, alpha: float = 0.5):
        trace = QueryTrace(query)

        if not query or not isinstance(query, str):
            return []

        alpha = max(0.0, min(1.0, alpha))

        bm25_results = []
        if self.bm25:
            try:
                bm25_results = self.bm25.search(query, top_k=top_k * 3)
            except Exception:
                bm25_results = []

        trace.add_stage("bm25", bm25_results)

        try:
            dense_results = self.store.search_dense(
                query=query,
                embedder=self.embedder,
                top_k=top_k * 3
            )
        except Exception:
            dense_results = []

        trace.add_stage("dense", dense_results)

        bm25_results = self._normalize_bm25(bm25_results)

        combined = {}

        for text, score in bm25_results:
            if not text:
                continue
            combined[text] = {
                "text": text,
                "bm25": float(score),
                "dense": 0.0,
                "source": "Uploaded PDF",
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
                }
            else:
                combined[text]["dense"] = float(r.get("score", 0.0))
                combined[text]["source"] = r.get("source", "Uploaded PDF")

        fused = []
        for item in combined.values():
            score = (alpha * item["dense"]) + ((1 - alpha) * item["bm25"])
            fused.append({
                "text": item["text"],
                "score": float(score),
                "source": item["source"],
            })

        fused.sort(key=lambda x: x["score"], reverse=True)
        trace.add_stage("fusion", fused)

        if self.reranker and fused:
            try:
                reranked = self.reranker.rerank(query, fused, top_k * 2)
                final = self._filter_reranked(reranked)[:top_k]
            except Exception:
                final = fused[:top_k]
        else:
            final = fused[:top_k]

        trace.add_stage("rerank", final)
        trace.set_final(final)
        self.logger.log_trace(trace.to_dict())

        return final

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