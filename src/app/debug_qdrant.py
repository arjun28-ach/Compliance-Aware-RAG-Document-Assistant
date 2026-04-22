# debug_qdrant.py

from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

print(client.get_collections())

points, _ = client.scroll(
    collection_name="documents",
    limit=10,
    with_payload=True,
    with_vectors=False
)

print("docs:", len(points))
print(points[0].payload if points else "empty")