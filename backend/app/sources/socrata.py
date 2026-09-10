from typing import Any

import httpx


class SocrataClient:
    def __init__(self, domain: str, dataset_id: str, timeout: float = 30.0):
        self.domain = domain
        self.dataset_id = dataset_id
        self.timeout = timeout

    @property
    def url(self) -> str:
        return f"https://{self.domain}/resource/{self.dataset_id}.json"

    async def get(self, params: dict[str, Any]) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise ValueError("Socrata response is not a list")
            return data
