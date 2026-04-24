from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.upload import router as upload_router

app = FastAPI(title="Compliance-Aware RAG Document Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://compliance-aware-rag-document-assis.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "RAG Assistant API is running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(upload_router)
app.include_router(chat_router)