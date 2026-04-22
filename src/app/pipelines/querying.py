class QueryPipeline:
    def __init__(self, retriever, llm_service):
        self.retriever = retriever
        self.llm_service = llm_service

    def run(self, query: str) -> dict:
        sources = self.retriever.search(query)
        answer = self.llm_service.generate_answer(query, sources)
        return {
            "query": query,
            "answer": answer,
            "sources": sources,
        }