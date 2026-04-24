from google import genai
from app.config import settings


class Embedder:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model = "gemini-embedding-001"

    def embed_query(self, query: str):
        response = self.client.models.embed_content(
            model=self.model,
            contents=query,
        )
        return response.embeddings[0].values

    def embed_documents(self, documents: list[str]):
        if not documents:
            return []

        response = self.client.models.embed_content(
            model=self.model,
            contents=documents,
        )

        return [embedding.values for embedding in response.embeddings]