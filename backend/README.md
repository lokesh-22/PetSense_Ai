# PetSense AI Backend

FastAPI backend for auth, multi-pet profiles, breed-aware chat retrieval, health tools, and ingredient scanning.

## Runtime

- PostgreSQL for core application data
- Redis for caching
- FAISS on local disk for breed knowledge retrieval
- FastAPI served locally by Uvicorn
- LangChain-based ingestion, retrieval, and response orchestration

## Run locally

```bash
docker compose up -d

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment

Use values from [.env.example](/Users/lokii/Documents/petApp/PetSense_Ai/backend/.env.example).

Important variables:

- `OPENAI_API_KEY` or `GROQ_API_KEY`
- `LLM_PROVIDER`
- `LLM_MODEL_NAME`
- `EMBEDDING_MODEL_NAME`
- `KNOWLEDGE_BASE_DIR`
- `FAISS_INDEX_DIR`

## Docker

Docker is used only for PostgreSQL and Redis via [docker-compose.yml](/Users/lokii/Documents/petApp/PetSense_Ai/docker-compose.yml).

## RAG Endpoints

- `POST /api/v1/ingest` rebuilds the FAISS index from `data/knowledge_base`
- `POST /api/v1/chat` streams chat responses with citations over SSE
- `GET /health` checks system status
