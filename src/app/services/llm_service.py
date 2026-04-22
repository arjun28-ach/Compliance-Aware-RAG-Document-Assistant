from google import genai
from app.config import settings


class LLMService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model = settings.LLM_MODEL

    def generate_answer(self, query: str, sources: list[dict]) -> str:
        if not sources:
            return "I could not find relevant information in the uploaded document."

        context = "\n\n---\n\n".join(
            [src["text"] for src in sources if src.get("text")]
        )

        prompt = f"""
You are a helpful document assistant.

Answer the user's question only using the provided context.
If the answer is not in the context, say you could not find it in the document.
Be concise and accurate.

Question:
{query}

Context:
{context}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return (response.text or "").strip()