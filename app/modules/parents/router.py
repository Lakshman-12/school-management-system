from fastapi import APIRouter, Query, status

from app.db.session import DB
from app.modules.auth.dependencies import AdminUser, CurrentUser
from app.modules.parents.schemas import (
    ParentCreate,
    ParentListResponse,
    ParentResponse,
    ParentUpdate,
)
from app.modules.parents.service import ParentService

router = APIRouter(
    prefix="/parents",
    tags=["Parents"],
)


@router.post(
    "/",
    response_model=ParentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_parent(
    parent_data: ParentCreate,
    db: DB,
    current_user: AdminUser,
):
    service = ParentService(db)
    return await service.create_parent(parent_data)


@router.get(
    "/",
    response_model=ParentListResponse,
)
async def get_parents(
    db: DB,
    current_user: AdminUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    is_active: bool | None = Query(None),
):
    service = ParentService(db)
    return await service.get_parents(
        page=page,
        page_size=page_size,
        is_active=is_active,
    )


@router.get(
    "/{parent_id}",
    response_model=ParentResponse,
)
async def get_parent_by_id(
    parent_id: int,
    db: DB,
    current_user: CurrentUser,
):
    service = ParentService(db)
    return await service.get_parent_by_id(parent_id)


@router.patch(
    "/{parent_id}",
    response_model=ParentResponse,
)
async def update_parent(
    parent_id: int,
    update_data: ParentUpdate,
    db: DB,
    current_user: AdminUser,
):
    service = ParentService(db)
    return await service.update_parent(parent_id, update_data)


@router.delete(
    "/{parent_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_parent(
    parent_id: int,
    db: DB,
    current_user: AdminUser,
):
    service = ParentService(db)
    return await service.deactivate_parent(parent_id)
