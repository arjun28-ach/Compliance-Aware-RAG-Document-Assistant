from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self):
        self.documents = []
        self.tokenized_corpus = []
        self.bm25 = None

    def build(self, documents):
        if not documents:
            self.documents = []
            self.tokenized_corpus = []
            self.bm25 = None
            return self

        self.documents = documents
        self.tokenized_corpus = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        return self

    def search(self, query, top_k=5):
        if not self.bm25 or not self.tokenized_corpus:
            return []

        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return ranked