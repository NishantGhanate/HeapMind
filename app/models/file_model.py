from typing import Optional

from app.models.common_model import CommonBaseModel


class FileModel(CommonBaseModel, table=True):
    __tablename__ = "file"

    file_name: str
    file_path: str
    files_ize: Optional[int] = None
    mime_type: Optional[str] = None
    checksum: Optional[str] = None
