from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    query: str


class ResultItem(BaseModel):
    text: str
    score: float


class ChatResponse(BaseModel):
    query: str
    results: List[ResultItem]
    error: Optional[str] = None