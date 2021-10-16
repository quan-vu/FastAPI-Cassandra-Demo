from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.responses.base_response import PaginationResponse


class OrganizationResponse(BaseModel):
    organization_id: UUID
    user_id: int
    name: str
    alias: str
    logo: str
    created_at: datetime
    updated_at: datetime


class OrganizationPaginationResponse(PaginationResponse):
    data: List[OrganizationResponse] = []


class SuccessDetailResponse(BaseModel):
    message: str = ''
    success: bool = True
    data: Optional[OrganizationResponse] = None


class SuccessPaginationResponse(BaseModel):
    message: str = ''
    success: bool = True
    data: Optional[OrganizationPaginationResponse] = None


class SuccessListResponse(BaseModel):
    message: str = ''
    success: bool = True
    data: List[OrganizationResponse] = None
