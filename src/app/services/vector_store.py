from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType,
)
import hashlib
#import uuid


class VectorStore:
    def __init__(self, client, collection_name: str):
        self.client = client
        self.collection_name = collection_name

    # -------------------------
    # Collection lifecycle
    # -------------------------
    def ensure_collection(self, vector_size: int):
        collections = self.client.get_collections().collections
        names = {c.name for c in collections}

        if self.collection_name not in names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

        # Required for Qdrant Cloud filtering
        self._ensure_payload_indexes()

    # -------------------------
    # Hashing
    # -------------------------
    def _hash_text(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    # -------------------------
    # Safe existence check
    # -------------------------
    def chunk_exists(self, chunk_hash: str) -> bool:
        result = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="chunk_hash",
                        match=MatchValue(value=chunk_hash)
                    )
                ]
            ),
            limit=1,
            with_payload=False,
            with_vectors=False,
        )

        points, _ = result
        return len(points) > 0

    # -------------------------
    # Insert documents (safe + deduplicated)
    # -------------------------
    def add_documents(self, chunks, embeddings, source_file):
        points = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_hash = self._hash_text(chunk)

            if self.chunk_exists(chunk_hash):
                continue

            points.append(
                PointStruct(
                    id=chunk_hash,
                    vector=embedding,
                    payload={
                        "text": chunk,
                        "source": source_file,
                        "chunk_hash": chunk_hash,
                    },
                )
            )

        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

    # -------------------------
    # Safe document retrieval
    # -------------------------
    def get_all_documents(self):
        all_docs = []
        offset = None

        while True:
            points, offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )

            for p in points:
                text = (p.payload or {}).get("text")
                if text:
                    all_docs.append(text)

            if offset is None:
                break

        return all_docs
    
    # -------------------------
    # Get documents by source (PDF/file level retrieval)
    # -------------------------
    def get_documents_by_source(self, doc_id: str):
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=doc_id)
                    )
                ]
            ),
            limit=100,
            with_payload=True,
            with_vectors=False,
        )

        return [
            p.payload["text"]
            for p in points
            if p.payload and "text" in p.payload
        ]
    
    # -------------------------
    # Dense vector search
    # -------------------------
    def search_dense(self, query: str, embedder, top_k: int = 5):
        query_vector = embedder.embed_query(query)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        points = results.points if hasattr(results, "points") else []

        return [
            {
                "text": (p.payload or {}).get("text"),
                "score": float(p.score),
                "source": (p.payload or {}).get("source"),
            }
            for p in points
            if p.payload and "text" in p.payload
        ]
    
    def _ensure_payload_indexes(self):
        indexes = [
            ("chunk_hash", PayloadSchemaType.KEYWORD),
            ("source", PayloadSchemaType.KEYWORD),
        ]

        for field_name, schema_type in indexes:
            try:
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name=field_name,
                    field_schema=schema_type,
                )
            except Exception:
                # Index may already exist. Do not crash startup.
                pass