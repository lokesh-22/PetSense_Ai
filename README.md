# PetSense AI

Pet health assistant with a local React + Vite frontend, local FastAPI backend, Dockerized PostgreSQL, Dockerized Redis, and a local FAISS vector store.

## Stack

- `petsenseai_frontend/`: React + Vite app run locally
- `backend/`: FastAPI API run locally
- `postgres`: Dockerized PostgreSQL for application data
- `redis`: Dockerized cache layer for breed/profile fetches
- `data/faiss_index/`: local FAISS index files and metadata
- `ai/`: reserved area for future model-specific modules
- `data/`: curated breed and ingredient source files

## Run Infra With Docker

```bash
docker compose up -d
```

Docker services:

- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## Run Backend Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend docs:

- [http://localhost:8000/docs](http://localhost:8000/docs)

## Run Frontend Locally

```bash
cd petsenseai_frontend
npm install
npm run dev
```

Frontend:

- [http://localhost:5173](http://localhost:5173)

## Notes

- PostgreSQL stores relational application data.
- Redis is included for phase 2 caching.
- Breed knowledge embeddings are stored locally in FAISS under `data/faiss_index/`.
