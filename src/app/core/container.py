from qdrant_client import QdrantClient

from app.config import settings
from app.services.vector_store import VectorStore
from app.services.embedder import Embedder
from app.services.hybrid_retriever import HybridRetriever
from app.services.bm25_retriever import BM25Retriever
#from app.services.reranker import Reranker


class Container:
    def __init__(self):
        self._client = None
        self._store = None
        self._embedder = None
        self._retriever = None

    # -------------------------
    # Qdrant Client
    # -------------------------
    def get_client(self):
        if self._client is None:
            self._client = QdrantClient(url=settings.QDRANT_URL)
        return self._client

    # -------------------------
    # Vector Store
    # -------------------------
    def get_store(self):
        if self._store is None:
            client = self.get_client()
            self._store = VectorStore(client, settings.COLLECTION_NAME)
            self._store.ensure_collection(vector_size=768)
        return self._store

    # -------------------------
    # Embedder
    # -------------------------
    def get_embedder(self):
        if self._embedder is None:
            self._embedder = Embedder()
        return self._embedder

    # -------------------------
    # Retriever
    # -------------------------
    def get_retriever(self):
        if self._retriever is None:
            store = self.get_store()
            embedder = self.get_embedder()

            bm25_builder = BM25Retriever()
            reranker = None

            self._retriever = HybridRetriever(
                vector_store=store,
                embedder=embedder,
                bm25_builder=bm25_builder,
                reranker=reranker
            )

            self._retriever.initialize()

        return self._retriever


# Global container (safe singleton)
container = Container()