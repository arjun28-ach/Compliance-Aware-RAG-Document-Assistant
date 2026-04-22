from pathlib import Path

from app.services.document_loader import load_pdf
from app.utils.chunker import chunk_text
from app.services.embedder import Embedder
from app.services.vector_store import VectorStore

DATA_PATH = "data/raw"


def ingest():
    embedder = Embedder()
    vector_store = VectorStore()

    # ✅ Ensure collection exists
    vector_store.create_collection()

    files = Path(DATA_PATH).glob("*.pdf")

    for file in files:
        print(f"\nProcessing: {file.name}")

        # 1. Load
        text = load_pdf(str(file))

        # 2. Chunk
        chunks = chunk_text(text)

        # 3. Embed
        embeddings = embedder.embed(chunks)

        # 4. Store (NEW)
        vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            source_file=file.name,
        )


if __name__ == "__main__":
    ingest()