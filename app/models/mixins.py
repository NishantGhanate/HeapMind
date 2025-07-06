from datetime import datetime
from typing import Optional, Type, TypeVar


T = TypeVar("T", bound="UpdateMixin")

class UpdateMixin:
    updated_at: Optional[datetime]

    @classmethod
    def apply_update(cls: Type[T], instance: T, **fields) -> T:
        for key, value in fields.items():
            setattr(instance, key, value)
        instance.updated_at = datetime.utcnow()
        return instance
