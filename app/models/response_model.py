from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    """
    Generic strucure for all
    """
    status_code: int
    message: str
    data: Optional[T] = None
