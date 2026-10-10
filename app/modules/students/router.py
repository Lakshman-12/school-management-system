from fastapi import APIRouter, Query, status

from app.db.session import DB
from app.modules.auth.dependencies import AdminUser, CurrentUser
from app.modules.students.schemas import (
    StudentCreate,
    StudentDetailResponse,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)
from app.modules.students.service import StudentService

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    student_data: StudentCreate,
    db: DB,
    current_user: AdminUser,
):
    service = StudentService(db)
    return await service.create_student(student_data)


@router.get(
    "/",
    response_model=StudentListResponse,
)
async def get_students(
    db: DB,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    class_id: int | None = Query(None),
    is_active: bool | None = Query(None),
):
    service = StudentService(db)
    return await service.get_students(
        page=page,
        page_size=page_size,
        class_id=class_id,
        is_active=is_active,
    )


@router.get(
    "/class/{class_id}",
    response_model=list[StudentResponse],
)
async def get_students_by_class(
    class_id: int,
    db: DB,
    current_user: CurrentUser,
):
    service = StudentService(db)
    return await service.get_students_by_class(class_id)


@router.get(
    "/parent/{parent_id}",
    response_model=list[StudentResponse],
)
async def get_students_by_parent(
    parent_id: int,
    db: DB,
    current_user: CurrentUser,
):
    service = StudentService(db)
    return await service.get_students_by_parent(parent_id)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
async def get_student_by_id(
    student_id: int,
    db: DB,
    current_user: CurrentUser,
):
    service = StudentService(db)
    return await service.get_student_by_id(student_id)


@router.get(
    "/{student_id}/detail",
    response_model=StudentDetailResponse,
)
async def get_student_detail(
    student_id: int,
    db: DB,
    current_user: CurrentUser,
):
    service = StudentService(db)
    return await service.get_student_detail(student_id)


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
)
async def update_student(
    student_id: int,
    update_data: StudentUpdate,
    db: DB,
    current_user: AdminUser,
):
    service = StudentService(db)
    return await service.update_student(student_id, update_data)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_student(
    student_id: int,
    db: DB,
    current_user: AdminUser,
):
    service = StudentService(db)
    return await service.deactivate_student(student_id)
