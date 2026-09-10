from datetime import datetime
from typing import Any

from app.models import Incident
from app.sources.base import SourceAdapter
from app.sources.socrata import SocrataClient


class LAPDCrimeAdapter(SourceAdapter):
    name = "Los Angeles Crime Data 2020-2024"
    provider = "LAPD / City of Los Angeles Open Data"
    dataset_id = "2nrs-mtv8"

    def __init__(self):
        self.client = SocrataClient("data.lacity.org", self.dataset_id)

    async def fetch(self, limit: int = 2000) -> list[dict[str, Any]]:
        # The LA dataset schema can evolve. This adapter deliberately keeps
        # the request conservative; validate the current fields before prod.
        return await self.client.get({"$limit": limit})

    def normalize(self, row: dict[str, Any]) -> Incident | None:
        date_value = (
            row.get("date_occ")
            or row.get("date_occurred")
            or row.get("date")
        )
        lat_value = row.get("lat") or row.get("latitude")
        lon_value = row.get("lon") or row.get("longitude")
        category = row.get("crm_cd_desc") or row.get("crime_type")

        if not date_value or lat_value is None or lon_value is None or not category:
            return None

        try:
            occurred_at = datetime.fromisoformat(str(date_value).replace("Z", "+00:00"))
            lat = float(lat_value)
            lon = float(lon_value)
        except (ValueError, TypeError):
            return None

        return Incident(
            source_record_id=str(row.get("dr_no") or row.get("id") or ""),
            occurred_at=occurred_at,
            latitude=lat,
            longitude=lon,
            category=str(category),
            metadata=row,
        )
