"""SafeHour ingestion jobs that persist normalized data to Supabase."""

import asyncio
from datetime import datetime, timezone

from app.db import supabase
from app.ingestion.dedupe import dedupe_incidents
from app.ingestion.normalize import fetch_normalized
from app.ingestion.quality import quality_report
from app.sources.chicago import ChicagoCrimeAdapter

CHICAGO_SOURCE_URL = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"


def _get_or_create_chicago_source() -> str:
    """Return the data_sources.id for the Chicago crime source."""
    city_result = (
        supabase.table("cities")
        .select("id")
        .eq("name", "Chicago")
        .eq("country", "USA")
        .limit(1)
        .execute()
    )

    if city_result.data:
        city_id = city_result.data[0]["id"]
    else:
        city_result = (
            supabase.table("cities")
            .insert(
                {
                    "name": "Chicago",
                    "country": "USA",
                    "region": "Illinois",
                    "latitude": 41.8781,
                    "longitude": -87.6298,
                    "timezone": "America/Chicago",
                }
            )
            .execute()
        )
        city_id = city_result.data[0]["id"]

    source_result = (
        supabase.table("data_sources")
        .select("id")
        .eq("city_id", city_id)
        .eq("dataset_id", "ijzp-q8t2")
        .limit(1)
        .execute()
    )

    if source_result.data:
        return source_result.data[0]["id"]

    source_result = (
        supabase.table("data_sources")
        .insert(
            {
                "city_id": city_id,
                "provider": "City of Chicago / Socrata",
                "source_url": CHICAGO_SOURCE_URL,
                "api_type": "Socrata",
                "dataset_id": "ijzp-q8t2",
                "status": "active",
            }
        )
        .execute()
    )
    return source_result.data[0]["id"]


def _incident_payload(source_id: str, incident) -> dict:
    return {
        "source_id": source_id,
        "source_record_id": incident.source_record_id,
        "occurred_at": incident.occurred_at.isoformat() if incident.occurred_at else None,
        "latitude": incident.latitude,
        "longitude": incident.longitude,
        "category": incident.category,
        "severity": incident.severity,
        "metadata": incident.metadata,
    }


def _upsert_in_batches(rows: list[dict], batch_size: int = 500) -> int:
    """Upsert incidents in small batches so a large sync remains reliable."""
    written = 0
    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        if not batch:
            continue
        result = (
            supabase.table("incidents")
            .upsert(batch, on_conflict="source_id,source_record_id")
            .execute()
        )
        written += len(result.data or batch)
    return written


async def run_chicago_sync(limit: int = 5000) -> dict:
    adapter = ChicagoCrimeAdapter()
    incidents = await fetch_normalized(adapter, limit=min(limit, 5000))
    incidents = dedupe_incidents(incidents)

    if not incidents:
        return {
            "city": "Chicago",
            "source": adapter.name,
            "fetched": 0,
            "written": 0,
            "quality": quality_report(incidents),
        }

    source_id = _get_or_create_chicago_source()
    rows = [_incident_payload(source_id, incident) for incident in incidents]
    written = _upsert_in_batches(rows)
    quality = quality_report(incidents)

    supabase.table("data_sources").update(
        {
            "status": "active",
            "quality_score": quality.get("score"),
            "last_successful_sync": datetime.now(timezone.utc).isoformat(),
            "last_schema_check": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", source_id).execute()

    return {
        "city": "Chicago",
        "source": adapter.name,
        "fetched": len(incidents),
        "written": written,
        "quality": quality,
    }


async def run_chicago_once() -> int:
    result = await run_chicago_sync(limit=5000)
    return result["written"]


if __name__ == "__main__":
    print(asyncio.run(run_chicago_sync()))
