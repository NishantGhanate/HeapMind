from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.config.settings import settings_config
from app.models.mixins import UpdateMixin


class CommonBaseModel(SQLModel, UpdateMixin):
    """
    Common to used across all sql models
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory= datetime.now(settings_config.tzinfo))
    updated_at: Optional[datetime] = None
