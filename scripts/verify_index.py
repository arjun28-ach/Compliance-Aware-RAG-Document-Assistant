from app.services.vector_store import VectorStore
from app.services.embedder import Embedder


def verify():
    store = VectorStore()
    embedder = Embedder()  # ✅ Step 1: initialize

    # 1. Collection info
    info = store.client.get_collection(store.collection_name)

    print("\n📊 COLLECTION INFO")
    print("-------------------")
    print(f"Collection Name: {store.collection_name}")
    print(f"Total Vectors: {info.points_count}")

    # 2. Create real query embedding
    query_text = "What is condition-based maintenance?"
    query_vector = embedder.embed([query_text])[0]  # ✅ Step 2

    print("\n🔍 SAMPLE SEARCH RESULTS")
    print("------------------------")
    print(f"Query: {query_text}")

    # 3. Search in Qdrant
    results = store.client.query_points(
        collection_name=store.collection_name,
        query=query_vector,  # ✅ Step 3 (correct param name)
        limit=5,
    )

    if not results.points:
        print("❌ No results found")
        return

    for i, r in enumerate(results.points):
        print(f"\nResult {i+1}")
        print(f"Score: {r.score}")
        print(f"Source: {r.payload.get('source')}")
        print(f"Preview: {r.payload.get('text')[:120]}...")


if __name__ == "__main__":
    verify()