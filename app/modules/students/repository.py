from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.classes.models import SchoolClass
from app.modules.parents.models import Parent
from app.modules.students.models import Student


class StudentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, student: Student) -> Student:
        try:
            self.db.add(student)
            await self.db.commit()
            await self.db.refresh(student)
            return student
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(self, student_id: int) -> Student | None:
        result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        return result.scalar_one_or_none()

    async def get_by_admission_number(
        self, admission_number: str
    ) -> Student | None:
        result = await self.db.execute(
            select(Student).where(
                Student.admission_number == admission_number
            )
        )
        return result.scalar_one_or_none()

    async def get_class_by_id(self, class_id: int) -> SchoolClass | None:
        result = await self.db.execute(
            select(SchoolClass).where(SchoolClass.id == class_id)
        )
        return result.scalar_one_or_none()

    async def get_parent_by_id(self, parent_id: int) -> Parent | None:
        result = await self.db.execute(
            select(Parent).where(Parent.id == parent_id)
        )
        return result.scalar_one_or_none()

    async def count(
        self,
        class_id: int | None = None,
        is_active: bool | None = None,
    ) -> int:
        stmt = select(func.count(Student.id))
        if class_id is not None:
            stmt = stmt.where(Student.class_id == class_id)
        if is_active is not None:
            stmt = stmt.where(Student.is_active == is_active)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_paginated(
        self,
        offset: int,
        limit: int,
        class_id: int | None = None,
        is_active: bool | None = None,
    ) -> list[Student]:
        stmt = select(Student).order_by(Student.id)
        if class_id is not None:
            stmt = stmt.where(Student.class_id == class_id)
        if is_active is not None:
            stmt = stmt.where(Student.is_active == is_active)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_student_detail(self, student_id: int):
        result = await self.db.execute(
            select(
                Student.id,
                Student.first_name,
                Student.last_name,
                Student.admission_number,
                Student.date_of_birth,
                Student.gender,
                Student.class_id,
                SchoolClass.name.label("class_name"),
                SchoolClass.section.label("class_section"),
                SchoolClass.academic_year.label("class_academic_year"),
                Student.parent_id,
                (Parent.first_name + " " + Parent.last_name).label("parent_name"),
                Parent.phone.label("parent_phone"),
                Student.is_active,
                Student.created_at,
                Student.updated_at,
            )
            .join(SchoolClass, Student.class_id == SchoolClass.id)
            .join(Parent, Student.parent_id == Parent.id)
            .where(Student.id == student_id)
        )
        return result.mappings().one_or_none()

    async def get_by_class(self, class_id: int) -> list[Student]:
        result = await self.db.execute(
            select(Student)
            .where(Student.class_id == class_id, Student.is_active == True)
            .order_by(Student.first_name, Student.last_name)
        )
        return list(result.scalars().all())

    async def get_by_parent(self, parent_id: int) -> list[Student]:
        result = await self.db.execute(
            select(Student)
            .where(Student.parent_id == parent_id, Student.is_active == True)
            .order_by(Student.first_name, Student.last_name)
        )
        return list(result.scalars().all())

    async def update(self, student: Student, update_data: dict) -> Student:
        try:
            for field, value in update_data.items():
                setattr(student, field, value)
            await self.db.commit()
            await self.db.refresh(student)
            return student
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, student: Student) -> None:
        try:
            student.is_active = False
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
