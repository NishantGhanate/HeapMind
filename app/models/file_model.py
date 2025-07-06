from typing import Optional

from app.models.common_model import CommonBaseModel


class FileModel(CommonBaseModel, table=True):
    filename: str
    filepath: str
    filesize: Optional[int] = None
    mime_type: Optional[str] = None
    checksum: Optional[str] = None
