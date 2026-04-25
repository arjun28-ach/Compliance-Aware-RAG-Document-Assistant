from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.dependencies import get_retriever
from app.services.llm_service import LLMService

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    doc_id: str


def extract_source_title(text: str) -> str:
    if not text:
        return "Relevant section"

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[0][:90] if lines else "Relevant section"


@router.post("/chat")
def chat(req: ChatRequest, retriever=Depends(get_retriever)):
    try:
        sources = retriever.search(
            query=req.query,
            doc_id=req.doc_id,
        )

        llm = LLMService()
        answer = llm.generate_answer(req.query, sources)

        clean_sources = [
            {
                "title": extract_source_title(s.get("text", "")),
                "text": s.get("text", "")[:320],
                "score": s.get("score"),
                "source": s.get("source", "Uploaded PDF"),
                "doc_id": s.get("doc_id"),
                "rerank_score": s.get("rerank_score"),
            }
            for s in sources[:3]
        ]

        return {
            "query": req.query,
            "doc_id": req.doc_id,
            "answer": answer,
            "sources": clean_sources,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")