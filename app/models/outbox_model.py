from datetime import datetime
import json
from typing import Optional
import uuid

from sqlmodel import Field

from app.models.common_model import CommonBaseModel


class OutboxEventModel(CommonBaseModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_type: str
    payload: str  # JSON-serialized payload
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)
    processed_at: Optional[datetime] = None
