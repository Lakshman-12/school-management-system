from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from math import ceil

from app.modules.auth.models import User, UserRole
from app.modules.teachers.models import Teacher
from app.modules.teachers.repository import TeacherRepository
from app.modules.teachers.schemas import AdminCreateTeacher,  TeacherSelfUpdate, AdminTeacherUpdate
from app.core.security import hash_password


class TeacherService:

    def __init__(self, db: AsyncSession):
        self.repository = TeacherRepository(db)

    async def create_teacher(
        self,
        teacher_data: AdminCreateTeacher,
    ) -> Teacher:

        # 1. Check whether the email already exists
        existing_user = await self.repository.get_user_by_email(
            teacher_data.email
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # 2. Hash the password
        hashed_password = hash_password(
            teacher_data.password
        )

        # 3. Create the User account
        user = User(
            email=teacher_data.email,
            password_hash=hashed_password,
            role=UserRole.TEACHER,
        )

        # 4. Create the Teacher profile
        teacher = Teacher(
            full_name=teacher_data.full_name,
            qualification=teacher_data.qualification,
            phone=teacher_data.phone,
        )

        # 5. Save both records through the Repository
        return await self.repository.create_with_user(
            user=user,
            teacher=teacher,
        )
        
        
        
        
    async def get_my_profile(
        self,
        user_id: int,
        ) -> Teacher:

        teacher = await self.repository.get_by_user_id(
            user_id
        )

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher profile not found",
            )

        return teacher
    
        
    async def get_all_teachers(self) -> list[Teacher]:
        return await self.repository.get_all()
    
    

    async def get_teacher_by_id(
        self,
        teacher_id: int,
    ) -> Teacher:

        teacher = await self.repository.get_by_id(
            teacher_id
        )

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found",
            )

        return teacher
    
    
    
    
    
    async def update_my_profile(
        self,
        user_id: int,
        update_data: TeacherSelfUpdate,
    ) -> Teacher:
        teacher = await self.repository.get_by_user_id(
            user_id
        )

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher profile not found",
            )

        data = update_data.model_dump(exclude_unset=True)

        return await self.repository.update(teacher, data)
    
    
    
    
        
    async def update_teacher(
        self,
        teacher_id: int,
        update_data: AdminTeacherUpdate,
    ) -> Teacher:
        teacher = await self.repository.get_by_id(
            teacher_id
        )

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found",
            )

        data = update_data.model_dump(exclude_unset=True)

        return await self.repository.update(teacher, data)
    
    
    
    
    
    @staticmethod
    async def get_teachers(
        db: AsyncSession,
        page: int,
        page_size: int,
    ):
        total = await TeacherRepository.count_teachers(db)

        offset = (page - 1) * page_size

        teachers = await TeacherRepository.get_teachers(
            db=db,
            offset=offset,
            limit=page_size,
        )

        pages = ceil(total / page_size) if total else 0

        return {
            "items": teachers,
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": pages,
        }

    async def deactivate_teacher(
        self,
        teacher_id: int,
    ) -> dict:
        teacher = await self.repository.get_by_id(teacher_id)

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found",
            )

        await self.repository.deactivate(teacher)

        return {
            "message": f"Teacher '{teacher.full_name}' deactivated successfully",
            "teacher_id": teacher.id,
        }