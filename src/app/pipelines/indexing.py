class IndexingPipeline:
    def __init__(self, ingestion_service, retriever):
        self.ingestion_service = ingestion_service
        self.retriever = retriever

    def run(self, file_bytes: bytes, filename: str) -> dict:
        result = self.ingestion_service.ingest(file_bytes=file_bytes, filename=filename)
        self.retriever.initialize()
        return result