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
import uuid


class VectorStore:
    def __init__(self, client, collection_name: str):
        self.client = client
        self.collection_name = collection_name

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

        self._ensure_payload_indexes()

    def _ensure_payload_indexes(self):
        indexes = [
            ("chunk_hash", PayloadSchemaType.KEYWORD),
            ("source", PayloadSchemaType.KEYWORD),
            ("doc_id", PayloadSchemaType.KEYWORD),
        ]

        for field_name, schema_type in indexes:
            try:
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name=field_name,
                    field_schema=schema_type,
                )
            except Exception:
                pass

    def _hash_text(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def chunk_exists(self, chunk_hash: str, doc_id: str) -> bool:
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="chunk_hash",
                        match=MatchValue(value=chunk_hash),
                    ),
                    FieldCondition(
                        key="doc_id",
                        match=MatchValue(value=doc_id),
                    ),
                ]
            ),
            limit=1,
            with_payload=False,
            with_vectors=False,
        )

        return len(points) > 0

    def add_documents(self, chunks, embeddings, source_file: str, doc_id: str):
        points = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_hash = self._hash_text(chunk)

            if self.chunk_exists(chunk_hash, doc_id):
                continue

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": chunk,
                        "source": source_file,
                        "doc_id": doc_id,
                        "chunk_hash": chunk_hash,
                    },
                )
            )

        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

    def get_documents_by_doc_id(self, doc_id: str):
        all_docs = []
        offset = None

        while True:
            points, offset = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="doc_id",
                            match=MatchValue(value=doc_id),
                        )
                    ]
                ),
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

    def search_dense(self, query: str, embedder, top_k: int = 5, doc_id: str | None = None):
        query_vector = embedder.embed_query(query)

        query_filter = None

        if doc_id:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="doc_id",
                        match=MatchValue(value=doc_id),
                    )
                ]
            )

        result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        points = result.points

        return [
            {
                "text": (point.payload or {}).get("text"),
                "score": float(point.score),
                "source": (point.payload or {}).get("source"),
                "doc_id": (point.payload or {}).get("doc_id"),
            }
            for point in points
            if point.payload and "text" in point.payload
        ]
    