from datetime import datetime
from typing import Optional

from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlmodel import Field, SQLModel

from app.config.settings import settings_config
from app.models.mixins import UpdateMixin


class CommonBaseModel(SQLModel, UpdateMixin):
    """
    Base model with id and timestamps.
    Each subclass gets its own Column instances.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(settings_config.tzinfo),
        sa_type=TIMESTAMP(timezone=True)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(settings_config.tzinfo),
        sa_type=TIMESTAMP(timezone=True)
    )
