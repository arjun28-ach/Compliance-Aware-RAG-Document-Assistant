from app.services.hybrid_retriever import HybridRetriever


def test_hybrid():
    retriever = HybridRetriever()

    query = "What is condition-based maintenance?"

    results = retriever.search(query, top_k=5, alpha=0.5)

    print("\n🔍 Hybrid Retrieval Results")
    print("----------------------------")
    print(f"Query: {query}")

    for i, r in enumerate(results):
        print(f"\nResult {i+1}")
        print(f"Score: {r['score']:.4f}")
        print(f"Preview: {r['text'][:120]}...")
        print(f"Rerank Score: {r.get('rerank_score', 0):.4f}")


if __name__ == "__main__":
    test_hybrid()