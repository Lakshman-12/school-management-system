from fastapi import APIRouter, status

from app.db.session import DB
from app.modules.auth.dependencies import AdminUser
from app.modules.teacher_assignments.schemas import (
    TeacherAssignmentCreate,
    TeacherAssignmentDetailResponse,
    TeacherAssignmentResponse,
)
from app.modules.teacher_assignments.service import (
    TeacherAssignmentService,
)


router = APIRouter(
    prefix="/teacher-assignments",
    tags=["Teacher Assignments"],
)


@router.post(
    "/",
    response_model=TeacherAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_teacher_assignment(
    data: TeacherAssignmentCreate,
    db: DB,
    current_user: AdminUser,
):
    return await TeacherAssignmentService.create_assignment(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[TeacherAssignmentDetailResponse],
)
async def get_all_assignments(
    db: DB,
    current_user: AdminUser,
):
    return await TeacherAssignmentService.get_all_assignments(db)


@router.delete(
    "/{assignment_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_teacher_assignment(
    assignment_id: int,
    db: DB,
    current_user: AdminUser,
):
    return await TeacherAssignmentService.delete_assignment(
        db,
        assignment_id,
    )

