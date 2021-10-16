from pydantic import BaseModel
from typing import Optional, List


class OrganizationCreateRequest(BaseModel):
    user_id: int
    name: str
    alias: str
    logo: Optional[str]


class OrganizationUpdateRequest(BaseModel):
    name: str
    alias: str
    logo: Optional[str]
