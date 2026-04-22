from app.services.vector_store import VectorStore
from app.services.bm25_retriever import BM25Retriever


def test_bm25():
    store = VectorStore()
    bm25 = BM25Retriever()

    # 1. Load documents from Qdrant
    documents = store.get_all_documents()

    print(f"Loaded {len(documents)} documents")

    # 2. Build BM25 index
    bm25.index(documents)

    # 3. Query
    query = "condition-based maintenance"

    results = bm25.search(query, top_k=5)

    print("\n🔍 BM25 Results:")
    for i, (doc, score) in enumerate(results):
        print(f"\nResult {i+1}")
        print(f"Score: {score}")
        print(f"Preview: {doc[:120]}...")


if __name__ == "__main__":
    test_bm25()