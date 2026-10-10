from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.classes.models import SchoolClass


class ClassRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, school_class: SchoolClass) -> SchoolClass:
        try:
            self.db.add(school_class)
            await self.db.commit()
            await self.db.refresh(school_class)
            return school_class
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(self, class_id: int) -> SchoolClass | None:
        result = await self.db.execute(
            select(SchoolClass).where(SchoolClass.id == class_id)
        )
        return result.scalar_one_or_none()

    async def get_by_unique(
        self, name: str, section: str, academic_year: str
    ) -> SchoolClass | None:
        result = await self.db.execute(
            select(SchoolClass).where(
                SchoolClass.name == name,
                SchoolClass.section == section,
                SchoolClass.academic_year == academic_year,
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[SchoolClass]:
        result = await self.db.execute(
            select(SchoolClass).order_by(SchoolClass.name, SchoolClass.section)
        )
        return list(result.scalars().all())

    async def update(
        self, school_class: SchoolClass, data: dict
    ) -> SchoolClass:
        try:
            for field, value in data.items():
                setattr(school_class, field, value)
            await self.db.commit()
            await self.db.refresh(school_class)
            return school_class
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, school_class: SchoolClass) -> None:
        try:
            await self.db.delete(school_class)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise