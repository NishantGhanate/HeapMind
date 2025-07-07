from typing import List, Optional

from pydantic import BaseModel


class SearchResult(BaseModel):
    chunk: str
    file_name: str
    file_path: str
    page_number: Optional[int] = None
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
