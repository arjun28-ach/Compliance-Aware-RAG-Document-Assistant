import fitz

from app.utils.chunker import TextChunker


class PDFIngestionService:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store
        self.chunker = TextChunker(chunk_size=800, overlap=120)

    def extract_text(self, file_bytes: bytes) -> str:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = [page.get_text() for page in doc]
        return "\n\n".join(pages).strip()

    def ingest(self, file_bytes: bytes, filename: str) -> dict:
        text = self.extract_text(file_bytes)

        if not text:
            return {"filename": filename, "chunks": 0, "status": "empty"}

        chunks = self.chunker.chunk(text)
        embeddings = self.embedder.embed_documents(chunks)

        self.vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            source_file=filename,
        )

        return {
            "filename": filename,
            "chunks": len(chunks),
            "status": "uploaded",
        }