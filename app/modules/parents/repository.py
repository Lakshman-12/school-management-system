from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.parents.models import Parent


class ParentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, parent: Parent) -> Parent:
        try:
            self.db.add(parent)
            await self.db.commit()
            await self.db.refresh(parent)
            return parent
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(self, parent_id: int) -> Parent | None:
        result = await self.db.execute(
            select(Parent).where(Parent.id == parent_id)
        )
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Parent | None:
        result = await self.db.execute(
            select(Parent).where(Parent.phone == phone)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Parent | None:
        result = await self.db.execute(
            select(Parent).where(Parent.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def count(self, is_active: bool | None = None) -> int:
        stmt = select(func.count(Parent.id))
        if is_active is not None:
            stmt = stmt.where(Parent.is_active == is_active)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_paginated(
        self,
        offset: int,
        limit: int,
        is_active: bool | None = None,
    ) -> list[Parent]:
        stmt = select(Parent).order_by(Parent.id)
        if is_active is not None:
            stmt = stmt.where(Parent.is_active == is_active)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update(self, parent: Parent, update_data: dict) -> Parent:
        try:
            for field, value in update_data.items():
                setattr(parent, field, value)
            await self.db.commit()
            await self.db.refresh(parent)
            return parent
        except Exception:
            await self.db.rollback()
            raise

    async def delete(self, parent: Parent) -> None:
        try:
            parent.is_active = False
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
