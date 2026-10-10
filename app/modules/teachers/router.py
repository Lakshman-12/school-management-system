from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import DB


from app.modules.auth.dependencies import AdminUser, TeacherUser
from app.modules.teachers.schemas import (
    AdminCreateTeacher,
    TeacherResponse,
    TeacherSelfUpdate,
    AdminTeacherUpdate,
    TeacherListResponse
)
from app.modules.teachers.service import TeacherService

from app.modules.teacher_assignments.schemas import (
    TeacherAssignmentDetailResponse,
)
from app.modules.teacher_assignments.service import (
    TeacherAssignmentService,
)


router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
)


@router.post(
    "/",
    response_model=TeacherResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_teacher(
    teacher_data: AdminCreateTeacher,
    db: DB,
    current_user: AdminUser,
):
    service = TeacherService(db)

    return await service.create_teacher(teacher_data)



@router.get(
    "/me",
    response_model=TeacherResponse,
)
async def get_my_profile(
    db: DB,
    current_user: TeacherUser,
):
    service = TeacherService(db)

    return await service.get_my_profile(
        current_user.id
    )
    
    
    

@router.get(
    "/",
    response_model=TeacherListResponse,
)
async def get_teachers(
    db: DB,
    current_user: AdminUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    return await TeacherService.get_teachers(
        db=db,
        page=page,
        page_size=page_size,
    )



@router.get(
    "/{teacher_id}",
    response_model=TeacherResponse,
)
async def get_teacher_by_id(
    teacher_id: int,
    db: DB,
    current_user: AdminUser,
):
    service = TeacherService(db)

    return await service.get_teacher_by_id(
        teacher_id
    )
    
    
    
    
    
@router.patch(
    "/me",
    response_model=TeacherResponse,
)
async def update_my_profile(
    update_data: TeacherSelfUpdate,
    db: DB,
    current_user: TeacherUser,
):
    service = TeacherService(db)

    return await service.update_my_profile(
        current_user.id,
        update_data,
    )
    
    
    

@router.patch(
    "/{teacher_id}",
    response_model=TeacherResponse,
)
async def update_teacher(
    teacher_id: int,
    update_data: AdminTeacherUpdate,
    db: DB,
    current_user: AdminUser,
):
    service = TeacherService(db)

    return await service.update_teacher(
        teacher_id,
        update_data,
    )
    
    

@router.get(
    "/me/assignments",
    response_model=list[TeacherAssignmentDetailResponse],
)
async def get_my_assignments(
    db: DB,
    current_user: TeacherUser,
):
    return await TeacherAssignmentService.get_my_assignments(
        db=db,
        user_id=current_user.id,
    )
    
    

@router.get(
    "/{teacher_id}/assignments",
    response_model=list[TeacherAssignmentDetailResponse],
)
async def get_teacher_assignments(
    teacher_id: int,
    db: DB,
    current_user: AdminUser,
):
    return await TeacherAssignmentService.get_teacher_assignments(
        db=db,
        teacher_id=teacher_id,
    )
    
    
    
    
    
@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_teacher(
    teacher_id: int,
    db: DB,
    current_user: AdminUser,
):
    service = TeacherService(db)
    return await service.deactivate_teacher(teacher_id)