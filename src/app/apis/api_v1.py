import json
from time import time
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Response, status

from app.requests.organization_request import OrganizationCreateRequest, OrganizationUpdateRequest
from app.repositories.base_cassandra_repository import Organization, OrganizationMember
from app.repositories.organization_repository import OrganizationRepository
from app.responses.organization_response import ( 
    SuccessPaginationResponse,
    SuccessDetailResponse,
)

from cassandra.cqlengine.management import sync_table


# Initial Application
app = FastAPI()
router = APIRouter()

@app.on_event("startup")
async def startup_event():
    sync_table(Organization)
    sync_table(OrganizationMember)

# API endpoints
@router.get("/check")
async def health_check(request: dict):
    start_time = time()
    duration_time = time() - start_time
    return {
        'duration': duration_time,
        'data': request
    }


@router.post("/", 
    response_model=SuccessDetailResponse,
    status_code=status.HTTP_201_CREATED
)
async def create(request: OrganizationCreateRequest):
    organization = OrganizationRepository().create(data=request)
    return {
        'message': 'Retrieve organization successfully', 
        'data': organization,
    }


@router.put("/{id}", response_model=SuccessDetailResponse)
async def update(id: str, request: OrganizationUpdateRequest):
    organization = OrganizationRepository().update(id=id, data=request)
    return {
        'message': 'Retrieve organization successfully', 
        'data': organization,
    }


@router.get("/", response_model=SuccessPaginationResponse)
async def paginate(limit: int=10, offset: str = None, search: str=''):
    organizations = OrganizationRepository().paginate(limit, offset, search)
    return {
        'message': 'Retrieve organizations successfully', 
        'data': organizations,
    }


@router.get("/{id}", response_model=SuccessDetailResponse)
async def detail(id: str):
    organization = OrganizationRepository().find(id)
    return {
        'message': 'Retrieve organization successfully', 
        'data': organization,
    }


# API Multiple Routers
app.include_router(router, prefix="/organizations", tags=["organizations"])
