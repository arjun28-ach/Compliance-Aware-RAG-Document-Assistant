from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.upload import router as upload_router
from app.middleware.logging import AuditLoggingMiddleware

app = FastAPI(title="RAG Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuditLoggingMiddleware)

@app.get("/")
def root():
    return {"status": "ok", "message": "RAG Assistant API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(upload_router)
app.include_router(chat_router)