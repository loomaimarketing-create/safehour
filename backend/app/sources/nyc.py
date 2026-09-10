from datetime import datetime
from typing import Any

from app.models import Incident
from app.sources.base import SourceAdapter
from app.sources.socrata import SocrataClient


class NYPDComplaintAdapter(SourceAdapter):
    name = "NYPD Complaint Data Historic"
    provider = "NYPD / NYC Open Data"
    dataset_id = "qgea-i56i"

    category_map = {
        "MURDER & NON-NEGL. MANSLAUGHTER": "HOMICIDE",
        "FELONY ASSAULT": "ASSAULT",
        "ROBBERY": "ROBBERY",
        "RAPE": "SEXUAL_ASSAULT",
    }

    def __init__(self):
        self.client = SocrataClient("data.cityofnewyork.us", self.dataset_id)

    async def fetch(self, limit: int = 2000) -> list[dict[str, Any]]:
        categories = ", ".join(f"'{x}'" for x in self.category_map)
        params = {
            "$where": f"ofns_desc IN ({categories}) AND latitude IS NOT NULL AND longitude IS NOT NULL",
            "$order": "cmplnt_fr_dt DESC",
            "$limit": limit,
        }
        return await self.client.get(params)

    def normalize(self, row: dict[str, Any]) -> Incident | None:
        date = row.get("cmplnt_fr_dt")
        time = row.get("cmplnt_fr_tm", "00:00:00")
        if not date:
            return None

        try:
            occurred_at = datetime.fromisoformat(f"{date}T{time}")
            lat = float(row["latitude"])
            lon = float(row["longitude"])
        except (ValueError, TypeError, KeyError):
            return None

        raw_category = row.get("ofns_desc", "UNKNOWN")
        return Incident(
            source_record_id=str(row.get("cmplnt_num", "")),
            occurred_at=occurred_at,
            latitude=lat,
            longitude=lon,
            category=self.category_map.get(raw_category, raw_category),
            metadata={
                "law_cat_cd": row.get("law_cat_cd"),
                "boro": row.get("boro_nm"),
                "premise": row.get("prem_typ_desc"),
            },
        )
