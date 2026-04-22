from pydantic import BaseModel
from typing import Optional, List


class SourceResponse(BaseModel):
    title: Optional[str] = None
    text: str
    score: Optional[float] = None
    rerank_score: Optional[float] = None
    source: Optional[str] = None


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceResponse]


class UploadResponse(BaseModel):
    filename: str
    chunks: int
    status: str