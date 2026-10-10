import math
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.students.models import Student
from app.modules.students.repository import StudentRepository
from app.modules.students.schemas import (
    StudentCreate,
    StudentDetailResponse,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)


class StudentService:

    def __init__(self, db: AsyncSession):
        self.repository = StudentRepository(db)

    async def create_student(self, student_data: StudentCreate) -> Student:
        existing = await self.repository.get_by_admission_number(
            student_data.admission_number
        )
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Student with admission number '{student_data.admission_number}' already exists",
            )

        school_class = await self.repository.get_class_by_id(
            student_data.class_id
        )
        if school_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Class with ID {student_data.class_id} not found",
            )

        parent = await self.repository.get_parent_by_id(student_data.parent_id)
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent with ID {student_data.parent_id} not found",
            )

        student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            admission_number=student_data.admission_number,
            date_of_birth=student_data.date_of_birth,
            gender=student_data.gender,
            class_id=student_data.class_id,
            parent_id=student_data.parent_id,
        )

        return await self.repository.create(student)

    async def get_student_by_id(self, student_id: int) -> Student:
        student = await self.repository.get_by_id(student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )
        return student

    async def get_student_detail(
        self, student_id: int
    ) -> StudentDetailResponse:
        detail = await self.repository.get_student_detail(student_id)
        if detail is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )
        return StudentDetailResponse(**dict(detail))

    async def get_students(
        self,
        page: int = 1,
        page_size: int = 10,
        class_id: int | None = None,
        is_active: bool | None = None,
    ) -> StudentListResponse:
        offset = (page - 1) * page_size
        total = await self.repository.count(
            class_id=class_id, is_active=is_active
        )
        items = await self.repository.get_paginated(
            offset=offset,
            limit=page_size,
            class_id=class_id,
            is_active=is_active,
        )
        pages = math.ceil(total / page_size) if total > 0 else 0

        return StudentListResponse(
            items=[StudentResponse.model_validate(s) for s in items],
            page=page,
            page_size=page_size,
            total=total,
            pages=pages,
        )

    async def get_students_by_class(
        self, class_id: int
    ) -> list[StudentResponse]:
        school_class = await self.repository.get_class_by_id(class_id)
        if school_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Class with ID {class_id} not found",
            )
        students = await self.repository.get_by_class(class_id)
        return [StudentResponse.model_validate(s) for s in students]

    async def get_students_by_parent(
        self, parent_id: int
    ) -> list[StudentResponse]:
        parent = await self.repository.get_parent_by_id(parent_id)
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent with ID {parent_id} not found",
            )
        students = await self.repository.get_by_parent(parent_id)
        return [StudentResponse.model_validate(s) for s in students]

    async def update_student(
        self,
        student_id: int,
        update_data: StudentUpdate,
    ) -> Student:
        student = await self.get_student_by_id(student_id)
        data = update_data.model_dump(exclude_unset=True)
        if not data:
            return student

        if "admission_number" in data:
            existing = await self.repository.get_by_admission_number(
                data["admission_number"]
            )
            if existing and existing.id != student_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Admission number '{data['admission_number']}' is already in use",
                )

        if "class_id" in data:
            school_class = await self.repository.get_class_by_id(
                data["class_id"]
            )
            if school_class is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Class with ID {data['class_id']} not found",
                )

        if "parent_id" in data:
            parent = await self.repository.get_parent_by_id(data["parent_id"])
            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent with ID {data['parent_id']} not found",
                )

        return await self.repository.update(student, data)

    async def deactivate_student(self, student_id: int) -> dict:
        student = await self.get_student_by_id(student_id)
        await self.repository.delete(student)
        return {
            "message": f"Student '{student.first_name} {student.last_name}' deactivated successfully",
            "student_id": student_id,
        }
