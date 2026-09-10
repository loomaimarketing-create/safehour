from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class Incident(BaseModel):
    source_record_id: str
    occurred_at: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category: str
    severity: Optional[int] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceStatus(BaseModel):
    name: str
    provider: str
    status: str
    dataset_id: Optional[str] = None
