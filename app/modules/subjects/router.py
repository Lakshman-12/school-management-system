from fastapi import APIRouter, status

from app.db.session import DB
from app.modules.auth.dependencies import AdminUser, CurrentUser
from app.modules.subjects.schemas import (
    SubjectCreate,
    SubjectResponse,
    SubjectUpdate,
)
from app.modules.subjects.service import SubjectService


router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


@router.post(
    "/",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_subject(
    subject_data: SubjectCreate,
    db: DB,
    current_user: AdminUser,
):
    service = SubjectService(db)
    return await service.create_subject(subject_data)


@router.get(
    "/",
    response_model=list[SubjectResponse],
)
async def get_all_subjects(
    db: DB,
    current_user: CurrentUser,
):
    service = SubjectService(db)
    return await service.get_all_subjects()


@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
)
async def get_subject_by_id(
    subject_id: int,
    db: DB,
    current_user: CurrentUser,
):
    service = SubjectService(db)
    return await service.get_subject_by_id(subject_id)


@router.patch(
    "/{subject_id}",
    response_model=SubjectResponse,
)
async def update_subject(
    subject_id: int,
    subject_data: SubjectUpdate,
    db: DB,
    current_user: AdminUser,
):
    service = SubjectService(db)
    return await service.update_subject(subject_id, subject_data)


@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_subject(
    subject_id: int,
    db: DB,
    current_user: AdminUser,
):
    service = SubjectService(db)
    return await service.delete_subject(subject_id)