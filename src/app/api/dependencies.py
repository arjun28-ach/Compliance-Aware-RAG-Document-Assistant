from qdrant_client import QdrantClient

from app.config import settings
from app.services.vector_store import VectorStore
from app.services.embedder import Embedder
from app.services.bm25_retriever import BM25Retriever
from app.services.hybrid_retriever import HybridRetriever
from app.services.reranker import Reranker


client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

vector_store = VectorStore(
    client=client,
    collection_name=settings.COLLECTION_NAME
)
vector_store.ensure_collection(vector_size=384)

embedder = Embedder()
bm25_builder = BM25Retriever()
reranker = Reranker()

retriever = HybridRetriever(
    vector_store=vector_store,
    embedder=embedder,
    bm25_builder=bm25_builder,
    reranker=reranker
)
retriever.initialize()


def get_vector_store():
    return vector_store


def get_embedder():
    return embedder


def get_retriever():
    return retriever