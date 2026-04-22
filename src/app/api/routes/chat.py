from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.dependencies import get_retriever
from app.services.llm_service import LLMService

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


def extract_source_title(text: str) -> str:
    if not text:
        return "Relevant section"

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines[:8]:
        if 4 <= len(line) <= 90:
            upper_ratio = sum(1 for ch in line if ch.isalpha() and ch.isupper()) / max(
                sum(1 for ch in line if ch.isalpha()), 1
            )
            if upper_ratio > 0.6:
                return line

            lowered = line.lower()
            keywords = [
                "abstract", "introduction", "conclusion", "results", "discussion",
                "methodology", "summary", "crop", "disease", "monitoring"
            ]
            if any(k in lowered for k in keywords):
                return line

    return lines[0][:90] if lines else "Relevant section"


@router.post("/chat")
def chat(req: ChatRequest, retriever=Depends(get_retriever)):
    try:
        sources = retriever.search(req.query)
        llm = LLMService()
        answer = llm.generate_answer(req.query, sources)

        clean_sources = [
            {
                "title": extract_source_title(s.get("text", "")),
                "text": s.get("text", "")[:320],
                "score": s.get("score"),
                "source": s.get("source", "Uploaded PDF"),
                "rerank_score": s.get("rerank_score"),
            }
            for s in sources[:3]
        ]

        return {
            "query": req.query,
            "answer": answer,
            "sources": clean_sources,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")