from fastapi import APIRouter, status

from app.db.session import DB
from app.modules.auth.dependencies import AdminUser, CurrentUser
from app.modules.classes.schemas import (
    ClassCreate,
    ClassResponse,
    ClassUpdate,
)
from app.modules.classes.service import ClassService


router = APIRouter(
    prefix="/classes",
    tags=["Classes"],
)


@router.post(
    "/",
    response_model=ClassResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_class(
    class_data: ClassCreate,
    db: DB,
    current_user: AdminUser,
):
    service = ClassService(db)
    return await service.create_class(class_data)


@router.get(
    "/",
    response_model=list[ClassResponse],
)
async def get_all_classes(
    db: DB,
    current_user: CurrentUser,
):
    service = ClassService(db)
    return await service.get_all_classes()


@router.get(
    "/{class_id}",
    response_model=ClassResponse,
)
async def get_class_by_id(
    class_id: int,
    db: DB,
    current_user: CurrentUser,
):
    service = ClassService(db)
    return await service.get_class_by_id(class_id)


@router.patch(
    "/{class_id}",
    response_model=ClassResponse,
)
async def update_class(
    class_id: int,
    class_data: ClassUpdate,
    db: DB,
    current_user: AdminUser,
):
    service = ClassService(db)
    return await service.update_class(class_id, class_data)


@router.delete(
    "/{class_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_class(
    class_id: int,
    db: DB,
    current_user: AdminUser,
):
    service = ClassService(db)
    return await service.delete_class(class_id)