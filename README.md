# SafeHour

SafeHour is a city-safety intelligence and navigation product built around **Time × Place**, with optional personalization and safety-aware routing.

## MVP focus

The first production milestone is:

Chicago official open data → ingestion → Supabase/Postgres → normalized incidents → hourly aggregation → FastAPI → frontend map.

The repository is intentionally structured so additional cities and data providers can be added through adapters.

## Repository

- `frontend/` — web app
- `backend/` — FastAPI API, ingestion, normalization and source adapters
- `database/` — Supabase/Postgres schema
- `docs/` — product and architecture documentation

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and configure values as needed.

### Frontend

The frontend is a lightweight Vite application.

```bash
cd frontend
npm install
npm run dev
```

## Important

The current repository is an MVP foundation. Chicago is the first fully defined source adapter. NYC and LA adapters are included as foundations and should be schema-validated before production ingestion.

Do not treat raw incident counts as individual crime probabilities. Safety scores should always expose confidence, sample size, period and source freshness.
