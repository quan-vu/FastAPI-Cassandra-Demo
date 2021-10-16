from typing import List
from pydantic import BaseModel


class PaginationResponse(BaseModel):
    total: int
    limit: int
    offset: str = None
    last_page: int
    next_page_link: str = None
    data: List = []
