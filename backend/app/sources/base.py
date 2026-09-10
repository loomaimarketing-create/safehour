from abc import ABC, abstractmethod
from typing import Any

from app.models import Incident


class SourceAdapter(ABC):
    name: str = "unknown"
    provider: str = "unknown"
    dataset_id: str | None = None

    @abstractmethod
    async def fetch(self, limit: int = 1000) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, row: dict[str, Any]) -> Incident | None:
        raise NotImplementedError
