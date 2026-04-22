from app.services.dense_retriever import DenseRetriever


def test_dense():
    retriever = DenseRetriever()

    query = "What is condition-based maintenance?"

    results = retriever.search(query, top_k=5)

    print("\n🔍 Dense Retrieval Results")
    print("--------------------------")

    for i, r in enumerate(results):
        print(f"\nResult {i+1}")
        print(f"Score (normalized): {r['score']:.4f}")
        print(f"Source: {r['source']}")
        print(f"Preview: {r['text'][:120]}...")


if __name__ == "__main__":
    test_dense()