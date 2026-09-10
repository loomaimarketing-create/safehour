"""Placeholder for scheduled production ingestion.

Next step:
- read source registry
- run adapters incrementally
- upsert into Supabase/Postgres
- persist sync status
- run quality checks
"""

import asyncio

from app.ingestion.dedupe import dedupe_incidents
from app.ingestion.normalize import fetch_normalized
from app.sources.chicago import ChicagoCrimeAdapter


async def run_chicago_once() -> int:
    adapter = ChicagoCrimeAdapter()
    incidents = await fetch_normalized(adapter, limit=5000)
    return len(dedupe_incidents(incidents))


if __name__ == "__main__":
    print(asyncio.run(run_chicago_once()))
