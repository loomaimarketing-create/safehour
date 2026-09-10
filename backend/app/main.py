from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.db import supabase
from app.discovery.discover import list_known_sources
from app.ingestion.dedupe import dedupe_incidents
from app.ingestion.normalize import fetch_normalized
from app.ingestion.quality import quality_report
from app.ingestion.runner import run_chicago_sync
from app.sources.chicago import ChicagoCrimeAdapter
from app.sources.la import LAPDCrimeAdapter
from app.sources.nyc import NYPDComplaintAdapter

app = FastAPI(
    title="SafeHour API",
    version="0.2.0",
    description="MVP API for city safety intelligence.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"name": "SafeHour API", "version": "0.2.0", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/db/health")
async def db_health():
    try:
        result = supabase.table("cities").select("id").limit(1).execute()
        return {"status": "connected", "rows_checked": len(result.data or [])}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Supabase connection failed: {exc}")


@app.get("/sources")
async def sources():
    return {"sources": list_known_sources()}


@app.get("/chicago/incidents")
async def chicago_incidents(limit: int = 500):
    adapter = ChicagoCrimeAdapter()
    incidents = await fetch_normalized(adapter, limit=min(limit, 5000))
    incidents = dedupe_incidents(incidents)

    return {
        "city": "Chicago",
        "source": adapter.name,
        "count": len(incidents),
        "quality": quality_report(incidents),
        "incidents": [item.model_dump(mode="json") for item in incidents],
    }


@app.get("/chicago/sync")
async def chicago_sync(limit: int = 5000):
    """Fetch Chicago incidents and upsert them into Supabase."""
    try:
        return await run_chicago_sync(limit=min(limit, 5000))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chicago sync failed: {exc}")


@app.get("/nyc/incidents")
async def nyc_incidents(limit: int = 500):
    adapter = NYPDComplaintAdapter()
    incidents = await fetch_normalized(adapter, limit=min(limit, 5000))
    incidents = dedupe_incidents(incidents)

    return {
        "city": "New York City",
        "source": adapter.name,
        "count": len(incidents),
        "quality": quality_report(incidents),
        "incidents": [item.model_dump(mode="json") for item in incidents],
    }


@app.get("/la/incidents")
async def la_incidents(limit: int = 500):
    adapter = LAPDCrimeAdapter()
    incidents = await fetch_normalized(adapter, limit=min(limit, 5000))
    incidents = dedupe_incidents(incidents)

    return {
        "city": "Los Angeles",
        "source": adapter.name,
        "count": len(incidents),
        "quality": quality_report(incidents),
        "incidents": [item.model_dump(mode="json") for item in incidents],
    }
