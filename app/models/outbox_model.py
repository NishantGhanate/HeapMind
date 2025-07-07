from datetime import datetime
import json
from typing import Optional
import uuid

from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlmodel import Field

from app.models.common_model import CommonBaseModel


class OutboxEventModel(CommonBaseModel, table=True):
    __tablename__ = "outbox_event"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_type: str
    payload: str  # JSON-serialized payload
    processed: bool = Field(default=False)
    processed_at: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True)
    )
