<div align="center">

<br />

```
██████╗  █████╗  ██████╗      █████╗ ███████╗███████╗██╗███████╗████████╗
██╔══██╗██╔══██╗██╔════╝     ██╔══██╗██╔════╝██╔════╝██║██╔════╝╚══██╔══╝
██████╔╝███████║██║  ███╗    ███████║███████╗███████╗██║███████╗   ██║
██╔══██╗██╔══██║██║   ██║    ██╔══██║╚════██║╚════██║██║╚════██║   ██║
██║  ██║██║  ██║╚██████╔╝    ██║  ██║███████║███████║██║███████║   ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝   ╚═╝
```

# Compliance-Aware RAG Document Assistant

**Production-grade Retrieval-Augmented Generation with AI Governance at its core**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14%2B-000000?style=flat-square&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![Haystack](https://img.shields.io/badge/Haystack-2.x-FF6B35?style=flat-square)](https://haystack.deepset.ai)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC244C?style=flat-square&logo=qdrant&logoColor=white)](https://qdrant.tech)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![EU AI Act](https://img.shields.io/badge/EU_AI_Act-Aligned-003399?style=flat-square)](https://artificialintelligenceact.eu)

<br />

> *Ask questions over private PDFs — and always know exactly why the AI answered the way it did.*

<br />

</div>

---

## Overview

This project is a **production-style RAG system** built for organizations and developers who need more than just answers — they need **traceable, auditable, explainable** AI. Every response is grounded in source documents with chunk-level attribution, relevance scoring, and a compliance-ready logging architecture inspired by **EU AI Act** governance principles.

No hallucinations. No black boxes. Just document-grounded answers you can stand behind.

---

## Features

| | Feature | Description |
|---|---|---|
| 📥 | **PDF Ingestion** | Upload and process documents through a clean UI |
| 🔍 | **Semantic Search** | Vector-based retrieval using Sentence Transformers |
| 🤖 | **Context-Aware QA** | LLM answers grounded strictly in retrieved context |
| 📚 | **Source Attribution** | Every answer links back to exact document chunks |
| 🧾 | **Chunk Traceability** | Section-level transparency on all responses |
| ⚖️ | **Compliance Logging** | AI Act-inspired audit trail for every inference |
| 🎯 | **Modern Chat UI** | Clean, responsive Next.js interface |
| 🔄 | **Session Management** | Stateful, multi-turn conversation support |

---

## System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────────────────┐
│   Browser   │────▶│   FastAPI    │────▶│   Haystack Pipeline   │
│  (Next.js)  │◀────│   Backend    │◀────│                       │
└─────────────┘     └──────────────┘     │  ┌─────────────────┐  │
                                         │  │  PDF Processor  │  │
                                         │  │  + Chunker      │  │
                                         │  └────────┬────────┘  │
                                         │           │            │
                                         │  ┌────────▼────────┐  │
                                         │  │  Embedder       │  │
                                         │  │  (SentenceT.)   │  │
                                         │  └────────┬────────┘  │
                                         │           │            │
                                         └───────────┼────────────┘
                                                     │
                                         ┌───────────▼────────────┐
                                         │     Qdrant Vector DB   │
                                         └───────────┬────────────┘
                                                     │
                                         ┌───────────▼────────────┐
                                         │  Retriever + Reranker  │
                                         │  (Cross-Encoder / Jina)│
                                         └───────────┬────────────┘
                                                     │
                                         ┌───────────▼────────────┐
                                         │       LLM Generator    │
                                         └───────────┬────────────┘
                                                     │
                                         ┌───────────▼────────────┐
                                         │  Answer + Sources      │
                                         │  + Compliance Log      │
                                         └────────────────────────┘
```

### Request Lifecycle

```
1. INGEST    PDF Upload ──▶ Chunking ──▶ Embedding ──▶ Store in Qdrant
2. QUERY     User Input ──▶ Embed Query ──▶ Vector Search ──▶ Top-K Chunks
3. RERANK    Retrieved Chunks ──▶ Cross-Encoder Reranker ──▶ Ordered Results
4. GENERATE  Ranked Context ──▶ LLM ──▶ Grounded Answer
5. RESPOND   Answer + Source Chunks + Scores + Audit Log ──▶ UI
```

---

## Tech Stack

### Backend

| Component | Technology | Purpose |
|---|---|---|
| **API Framework** | FastAPI | REST endpoints, async support |
| **Orchestration** | Haystack 2.x | Pipeline-based RAG composition |
| **Vector Store** | Qdrant | High-performance similarity search |
| **Embeddings** | Sentence Transformers | Local, privacy-preserving embeddings |
| **Reranker** | Cross-Encoder / Jina | Precision-boosted result ordering |
| **Validation** | Pydantic v2 | Strict schema enforcement |

### Frontend

| Component | Technology | Purpose |
|---|---|---|
| **Framework** | Next.js 14 (App Router) | Server-side + client rendering |
| **Styling** | TailwindCSS | Utility-first responsive design |
| **State** | React Hooks | Local session and UI state |

### AI & NLP

| Component | Technology |
|---|---|
| Text Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (or configurable) |
| Reranking | `cross-encoder/ms-marco-MiniLM` / Jina Reranker |
| Generation | OpenAI-compatible / local LLM endpoint |

---

## Project Structure

```
rag-document-assistant/
├── frontend/              # Next.js client
├── src/app/
│   ├── api/               # FastAPI routes and dependencies
│   ├── services/          # Retrieval, embedding, reranking, LLM
│   ├── pipelines/         # Indexing and query orchestration
│   ├── models/            # Request/response schemas
│   ├── compliance/        # Audit logging
│   ├── observability/     # Tracing and query logging
│   ├── utils/             # Chunking and evaluation helpers
│   ├── config.py          # App settings
│   └── main.py            # FastAPI entrypoint
├── data/                  # Test and uploaded PDFs
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md

```

---

## Setup & Installation

### Prerequisites

- Python **3.10+**
- Node.js **18+**
- Docker (for Qdrant)
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/arjun28-ach/Compliance-Aware-RAG-Document-Assistant.git
cd RAG-ASSISTANT
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your LLM API key and settings
```

Start the development server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API documentation will be available at `http://localhost:8000/docs`

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The UI will be available at `http://localhost:3000`

---

### 4. Start Qdrant (Vector Database)

Using Docker:

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

Qdrant dashboard: `http://localhost:6333/dashboard`

---

### 5. Full Stack with Docker Compose

Spin everything up in one command:

```bash
docker-compose up --build
```

---

### Environment Variables

Copy `.env.example` and configure:

```env
# LLM Configuration
LLM_PROVIDER=openai                     # openai | anthropic | local
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o-mini

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=rag_documents

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Reranker (optional)
RERANKER_ENABLED=true
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

# Compliance
AUDIT_LOG_PATH=./logs/audit.jsonl
AUDIT_LOG_ENABLED=true
```

---

## Usage

1. **Upload a document** — Drag and drop any PDF into the upload zone
2. **Wait for indexing** — The system chunks, embeds, and stores the document
3. **Ask questions** in natural language:
   - *"What is this document about?"*
   - *"Summarize the key findings in Section 3"*
   - *"What risks are identified and how are they mitigated?"*
4. **Review the response**:
   - ✅ Generated answer
   - 📄 Source chunks with section labels
   - 📊 Relevance scores per chunk

---

## Example Response

**Question:**
```
What is this document about?
```

**Answer:**
```
This document explores computer vision applications in precision agriculture,
covering methods for automated crop growth monitoring, disease detection using
aerial imagery, and yield prediction models trained on multi-spectral data.
```

**Sources:**

| # | Section | Score | Snippet |
|---|---|---|---|
| 1 | Introduction → Scope | `0.94` | *"...focuses on vision-based systems for autonomous field monitoring..."* |
| 2 | Chapter 2 → Crop Growth | `0.89` | *"...NDVI-based time series analysis enables early growth stage detection..."* |
| 3 | Chapter 4 → Disease Monitoring | `0.81` | *"...CNN classifiers achieve 96.2% accuracy on the PlantVillage benchmark..."* |

---

## AI Governance & Compliance

This system is architected with **EU AI Act principles** and responsible AI deployment in mind:

| Principle | Implementation |
|---|---|
| ✅ **Source Traceability** | Every answer maps to exact document chunks with metadata |
| ✅ **Explainable Outputs** | Relevance scores and retrieval reasoning exposed to the user |
| ✅ **No Blind Generation** | LLM is strictly context-bound — no hallucination-style responses |
| ✅ **Audit Logging** | Structured JSONL audit trail per inference (query, context, answer, scores) |
| ✅ **Auditable Pipelines** | Haystack's declarative pipeline format supports inspection and versioning |
| ✅ **Human Oversight Ready** | Architecture supports human-in-the-loop review integration |

### Audit Log Schema

```json
{
  "timestamp": "2025-01-15T10:32:01Z",
  "session_id": "abc-123",
  "query": "What are the identified risks?",
  "retrieved_chunks": 3,
  "top_score": 0.94,
  "model_used": "gpt-4o-mini",
  "answer_length": 312,
  "sources": ["doc_001:chunk_14", "doc_001:chunk_22"]
}
```

---

## API Reference

### `POST /api/upload`
Upload and index a PDF document.

```json
// Request (multipart/form-data)
{ "file": "<pdf_binary>" }

// Response
{ "document_id": "doc_abc123", "chunks_indexed": 47, "status": "ready" }
```

### `POST /api/query`
Ask a question over indexed documents.

```json
// Request
{ "question": "What are the key findings?", "session_id": "sess_xyz" }

// Response
{
  "answer": "The study identifies three primary findings...",
  "sources": [
    { "chunk_id": "doc_abc123:14", "section": "Results", "score": 0.93, "text": "..." }
  ],
  "model": "gpt-4o-mini",
  "latency_ms": 842
}
```

---

## Roadmap

- [ ] 🔐 Multi-user document isolation and access control
- [ ] 🧾 Full AI Act compliance logging dashboard (UI)
- [ ] 🧠 Hybrid search — BM25 + dense vector retrieval
- [ ] 📊 RAG evaluation metrics (RAGAS / DeepEval integration)
- [ ] 🗂 Document versioning and diff tracking
- [ ] ☁️ Production Docker + CI/CD pipeline (GitHub Actions)
- [ ] 🌐 Multi-language document support
- [ ] 🔌 LLM provider abstraction (OpenAI / Anthropic / Ollama)

---

## Contributing

Contributions are welcome! Please follow this workflow:

```bash
# 1. Fork the repository on GitHub
# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes and commit
git commit -m "feat: add your feature description"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

Please make sure your PR:
- Passes all existing tests
- Includes tests for new functionality
- Follows the existing code style
- Updates documentation where relevant

---

## Author

**Arjun Acharya**
*AI Engineer · RAG Systems · AI Governance*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/arjunacharya55/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/arjun28-ach)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**If this project helped you, give it a ⭐ and share your feedback!**

*Built with care for transparent, trustworthy AI systems.*

</div>