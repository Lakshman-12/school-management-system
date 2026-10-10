from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.subjects.models import Subject


class SubjectRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(
        self,
        name: str,
    ) -> Subject | None:
        result = await self.db.execute(
            select(Subject).where(
                Subject.name == name
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        subject: Subject,
    ) -> Subject:
        try:
            self.db.add(subject)
            await self.db.commit()
            await self.db.refresh(subject)
            return subject
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(self, subject_id: int) -> Subject | None:
        result = await self.db.execute(
            select(Subject).where(Subject.id == subject_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Subject]:
        result = await self.db.execute(
            select(Subject).order_by(Subject.name)
        )
        return list(result.scalars().all())

    async def update(self, subject: Subject, name: str) -> Subject:
        try:
            subject.name = name
            await self.db.commit()
            await self.db.refresh(subject)
            return subject
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, subject: Subject) -> None:
        try:
            await self.db.delete(subject)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise