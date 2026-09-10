from app.models import Incident
from app.sources.base import SourceAdapter


async def fetch_normalized(
    adapter: SourceAdapter,
    limit: int = 1000,
) -> list[Incident]:
    rows = await adapter.fetch(limit=limit)
    incidents: list[Incident] = []

    for row in rows:
        incident = adapter.normalize(row)
        if incident and incident.source_record_id:
            incidents.append(incident)

    return incidents
