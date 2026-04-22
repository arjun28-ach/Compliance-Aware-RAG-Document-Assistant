from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    # -------------------------
    # Query embedding (search)
    # -------------------------
    def embed_query(self, query: str):
        return self.model.encode(query).tolist()

    # -------------------------
    # Batch embedding (ingestion)
    # -------------------------
    def embed_documents(self, documents: list[str]):
        if not documents:
            return []

        return self.model.encode(documents).tolist()