from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.api.dependencies import get_vector_store, get_embedder, get_retriever
from app.services.pdf_ingestion import PDFIngestionService

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    vector_store=Depends(get_vector_store),
    embedder=Depends(get_embedder),
    retriever=Depends(get_retriever),
):
    try:
        contents = await file.read()

        ingestion_service = PDFIngestionService(
            embedder=embedder,
            vector_store=vector_store,
        )

        result = ingestion_service.ingest(
            file_bytes=contents,
            filename=file.filename,
        )

        retriever.initialize()

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")