# HireMindAI Backend

FastAPI backend scaffold for HireMindAI with PostgreSQL, Alembic, JWT auth, LangGraph/LangChain workflow hooks, Gemini API support, Qdrant vector search, local storage, and Docker.

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

API docs:

```text
http://localhost:8000/docs
```

Agents:

```text
GET  /api/v1/agents
POST /api/v1/agents/{agent_name}/run
```

## Workflow

The initial AI workflow lives in `app/workflows/candidate_screening.py`.
It currently performs:

1. Normalize candidate/job input
2. Analyze candidate fit
3. Generate recommendation

The Gemini call is isolated in `app/ai/llm.py` so the workflow can be tested or swapped later.
