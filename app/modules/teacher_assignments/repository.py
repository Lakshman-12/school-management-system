from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.teacher_assignments.models import TeacherAssignment
from app.modules.teachers.models import Teacher
from app.modules.classes.models import SchoolClass
from app.modules.subjects.models import Subject


class TeacherAssignmentRepository:

    @staticmethod
    async def get_teacher_by_id(
        db: AsyncSession,
        teacher_id: int,
    ) -> Teacher | None:
        result = await db.execute(
            select(Teacher).where(Teacher.id == teacher_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_class_by_id(
        db: AsyncSession,
        class_id: int,
    ) -> SchoolClass | None:
        result = await db.execute(
            select(SchoolClass).where(SchoolClass.id == class_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_subject_by_id(
        db: AsyncSession,
        subject_id: int,
    ) -> Subject | None:
        result = await db.execute(
            select(Subject).where(Subject.id == subject_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_assignment(
        db: AsyncSession,
        teacher_id: int,
        class_id: int,
        subject_id: int,
    ) -> TeacherAssignment | None:
        result = await db.execute(
            select(TeacherAssignment).where(
                TeacherAssignment.teacher_id == teacher_id,
                TeacherAssignment.class_id == class_id,
                TeacherAssignment.subject_id == subject_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db: AsyncSession,
        assignment: TeacherAssignment,
    ) -> TeacherAssignment:
        try:
            db.add(assignment)
            await db.commit()
            await db.refresh(assignment)

            return assignment

        except Exception:
            await db.rollback()
            raise
        
        
        
        

    @staticmethod
    async def get_teacher_assignments_with_details(
        db: AsyncSession,
        teacher_id: int,
    ):
        result = await db.execute(
            select(
                TeacherAssignment.id,
                TeacherAssignment.teacher_id,
                SchoolClass.name.label("class_name"),
                SchoolClass.section,
                SchoolClass.academic_year,
                Subject.name.label("subject_name"),
            )
            .join(
                SchoolClass,
                TeacherAssignment.class_id == SchoolClass.id,
            )
            .join(
                Subject,
                TeacherAssignment.subject_id == Subject.id,
            )
            .where(
                TeacherAssignment.teacher_id == teacher_id
            )
            .order_by(
                SchoolClass.name,
                SchoolClass.section,
                Subject.name,
            )
        )

        return result.mappings().all()
    
    
    @staticmethod
    async def get_teacher_by_user_id(
        db: AsyncSession,
        user_id: int,
    ) -> Teacher | None:
        result = await db.execute(
            select(Teacher).where(Teacher.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        assignment_id: int,
    ) -> TeacherAssignment | None:
        result = await db.execute(
            select(TeacherAssignment).where(TeacherAssignment.id == assignment_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_with_details(db: AsyncSession):
        result = await db.execute(
            select(
                TeacherAssignment.id,
                TeacherAssignment.teacher_id,
                Teacher.full_name.label("teacher_name"),
                SchoolClass.name.label("class_name"),
                SchoolClass.section,
                SchoolClass.academic_year,
                Subject.name.label("subject_name"),
            )
            .join(Teacher, TeacherAssignment.teacher_id == Teacher.id)
            .join(SchoolClass, TeacherAssignment.class_id == SchoolClass.id)
            .join(Subject, TeacherAssignment.subject_id == Subject.id)
            .order_by(
                Teacher.full_name,
                SchoolClass.name,
                SchoolClass.section,
                Subject.name,
            )
        )
        return result.mappings().all()

    @staticmethod
    async def delete(
        db: AsyncSession,
        assignment: TeacherAssignment,
    ) -> None:
        try:
            await db.delete(assignment)
            await db.commit()
        except Exception:
            await db.rollback()
            raise