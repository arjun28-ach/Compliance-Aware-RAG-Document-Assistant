from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import fitz

from app.api.dependencies import get_vector_store, get_embedder, get_retriever

router = APIRouter()


def extract_text(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    vector_store=Depends(get_vector_store),
    embedder=Depends(get_embedder),
    retriever=Depends(get_retriever),
):
    try:
        contents = await file.read()

        text = extract_text(contents)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in PDF")

        chunks = chunk_text(text)
        embeddings = embedder.embed_documents(chunks)

        vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            source_file=file.filename,
        )

        retriever.initialize()

        return {
            "filename": file.filename,
            "chunks": len(chunks),
            "status": "uploaded"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")