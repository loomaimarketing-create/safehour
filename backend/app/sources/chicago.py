from datetime import datetime
from typing import Any

from app.models import Incident
from app.sources.base import SourceAdapter
from app.sources.socrata import SocrataClient


class ChicagoCrimeAdapter(SourceAdapter):
    name = "Chicago Crimes - 2001 to Present"
    provider = "City of Chicago / Socrata"
    dataset_id = "ijzp-q8t2"

    categories = (
        "HOMICIDE",
        "CRIM SEXUAL ASSAULT",
        "ROBBERY",
        "ASSAULT",
        "BATTERY",
        "KIDNAPPING",
        "ARSON",
    )

    def __init__(self):
        self.client = SocrataClient("data.cityofchicago.org", self.dataset_id)

    async def fetch(self, limit: int = 5000) -> list[dict[str, Any]]:
        category_filter = ", ".join(f"'{x}'" for x in self.categories)
        params = {
            "$where": (
                "date >= '2025-01-01T00:00:00' "
                f"AND primary_type IN ({category_filter}) "
                "AND latitude IS NOT NULL AND longitude IS NOT NULL"
            ),
            "$order": "date DESC",
            "$limit": limit,
        }
        return await self.client.get(params)

    def normalize(self, row: dict[str, Any]) -> Incident | None:
        try:
            occurred_at = datetime.fromisoformat(
                row["date"].replace("Z", "+00:00")
            )
            lat = float(row["latitude"])
            lon = float(row["longitude"])
        except (KeyError, ValueError, TypeError):
            return None

        return Incident(
            source_record_id=str(row.get("id", "")),
            occurred_at=occurred_at,
            latitude=lat,
            longitude=lon,
            category=str(row.get("primary_type", "UNKNOWN")),
            metadata={
                "description": row.get("description"),
                "location_description": row.get("location_description"),
                "district": row.get("district"),
                "ward": row.get("ward"),
            },
        )
