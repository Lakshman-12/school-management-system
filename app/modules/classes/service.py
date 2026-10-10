from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.classes.models import SchoolClass
from app.modules.classes.repository import ClassRepository
from app.modules.classes.schemas import ClassCreate, ClassUpdate


class ClassService:

    def __init__(self, db: AsyncSession):
        self.repository = ClassRepository(db)

    async def create_class(
        self,
        class_data: ClassCreate,
    ) -> SchoolClass:
        existing = await self.repository.get_by_unique(
            name=class_data.name,
            section=class_data.section,
            academic_year=class_data.academic_year,
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Class '{class_data.name}-{class_data.section}' for academic year '{class_data.academic_year}' already exists",
            )

        school_class = SchoolClass(
            name=class_data.name,
            section=class_data.section,
            academic_year=class_data.academic_year,
        )

        return await self.repository.create(school_class)

    async def get_all_classes(self) -> list[SchoolClass]:
        return await self.repository.get_all()

    async def get_class_by_id(self, class_id: int) -> SchoolClass:
        school_class = await self.repository.get_by_id(class_id)
        if school_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found",
            )
        return school_class

    async def update_class(
        self, class_id: int, update_data: ClassUpdate
    ) -> SchoolClass:
        school_class = await self.get_class_by_id(class_id)

        data = update_data.model_dump(exclude_unset=True)
        if not data:
            return school_class

        target_name = data.get("name", school_class.name)
        target_section = data.get("section", school_class.section)
        target_year = data.get("academic_year", school_class.academic_year)

        existing = await self.repository.get_by_unique(
            target_name, target_section, target_year
        )
        if existing and existing.id != class_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Class '{target_name}-{target_section}' for '{target_year}' already exists",
            )

        return await self.repository.update(school_class, data)

    async def delete_class(self, class_id: int) -> dict:
        school_class = await self.get_class_by_id(class_id)
        await self.repository.delete(school_class)
        return {
            "message": f"Class '{school_class.name}-{school_class.section}' deleted successfully",
            "class_id": class_id,
        }