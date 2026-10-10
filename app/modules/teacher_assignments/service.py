from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.teacher_assignments.models import TeacherAssignment
from app.modules.teacher_assignments.repository import (
    TeacherAssignmentRepository,
)
from app.modules.teacher_assignments.schemas import (
    TeacherAssignmentCreate,
)


class TeacherAssignmentService:

    @staticmethod
    async def create_assignment(
        db: AsyncSession,
        data: TeacherAssignmentCreate,
    ) -> TeacherAssignment:

        # 1. Check whether the teacher exists
        teacher = await TeacherAssignmentRepository.get_teacher_by_id(
            db,
            data.teacher_id,
        )

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found",
            )

        # 2. Check whether the class exists
        school_class = await TeacherAssignmentRepository.get_class_by_id(
            db,
            data.class_id,
        )

        if school_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found",
            )

        # 3. Check whether the subject exists
        subject = await TeacherAssignmentRepository.get_subject_by_id(
            db,
            data.subject_id,
        )

        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )

        # 4. Check for a duplicate assignment
        existing_assignment = (
            await TeacherAssignmentRepository.get_assignment(
                db,
                data.teacher_id,
                data.class_id,
                data.subject_id,
            )
        )

        if existing_assignment is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This teacher assignment already exists",
            )

        # 5. Create the assignment
        assignment = TeacherAssignment(
            teacher_id=data.teacher_id,
            class_id=data.class_id,
            subject_id=data.subject_id,
        )

        # 6. Save through the repository
        return await TeacherAssignmentRepository.create(
            db,
            assignment,
        )
        
        
        
    @staticmethod
    async def get_my_assignments(
        db: AsyncSession,
        user_id: int,
    ):
        # 1. Find the teacher profile linked to the logged-in user
        teacher = await TeacherAssignmentRepository.get_teacher_by_user_id(
            db,
            user_id,
        )

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher profile not found",
            )

        # 2. Fetch the teacher's classes and subjects
        return await TeacherAssignmentRepository.get_teacher_assignments_with_details(
            db,
            teacher.id,
        )
        
        
        
        
    @staticmethod
    async def get_teacher_assignments(
        db: AsyncSession,
        teacher_id: int,
    ):
        # 1. Check whether the teacher exists
        teacher = await TeacherAssignmentRepository.get_teacher_by_id(
            db,
            teacher_id,
        )

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found",
            )

        # 2. Fetch the teacher's assignments
        return await TeacherAssignmentRepository.get_teacher_assignments_with_details(
            db,
            teacher_id,
        )

    @staticmethod
    async def get_all_assignments(db: AsyncSession):
        return await TeacherAssignmentRepository.get_all_with_details(db)

    @staticmethod
    async def delete_assignment(
        db: AsyncSession,
        assignment_id: int,
    ) -> dict:
        assignment = await TeacherAssignmentRepository.get_by_id(db, assignment_id)
        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher assignment not found",
            )
        await TeacherAssignmentRepository.delete(db, assignment)
        return {
            "message": "Teacher assignment removed successfully",
            "assignment_id": assignment_id,
        }