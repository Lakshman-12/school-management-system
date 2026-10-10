from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.subjects.models import Subject
from app.modules.subjects.repository import SubjectRepository
from app.modules.subjects.schemas import SubjectCreate, SubjectUpdate


class SubjectService:

    def __init__(self, db: AsyncSession):
        self.repository = SubjectRepository(db)

    async def create_subject(
        self,
        subject_data: SubjectCreate,
    ) -> Subject:
        clean_name = subject_data.name.strip()
        existing_subject = await self.repository.get_by_name(clean_name)

        if existing_subject is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Subject already exists",
            )

        subject = Subject(name=clean_name)

        return await self.repository.create(subject)

    async def get_all_subjects(self) -> list[Subject]:
        return await self.repository.get_all()

    async def get_subject_by_id(self, subject_id: int) -> Subject:
        subject = await self.repository.get_by_id(subject_id)
        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        return subject

    async def update_subject(
        self,
        subject_id: int,
        update_data: SubjectUpdate,
    ) -> Subject:
        subject = await self.get_subject_by_id(subject_id)
        clean_name = update_data.name.strip()

        existing = await self.repository.get_by_name(clean_name)
        if existing and existing.id != subject_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Subject '{clean_name}' already exists",
            )

        return await self.repository.update(subject, clean_name)

    async def delete_subject(self, subject_id: int) -> dict:
        subject = await self.get_subject_by_id(subject_id)
        await self.repository.delete(subject)
        return {
            "message": f"Subject '{subject.name}' deleted successfully",
            "subject_id": subject_id,
        }