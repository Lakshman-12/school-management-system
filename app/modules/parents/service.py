import math
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.parents.models import Parent
from app.modules.parents.repository import ParentRepository
from app.modules.parents.schemas import (
    ParentCreate,
    ParentListResponse,
    ParentResponse,
    ParentUpdate,
)


class ParentService:

    def __init__(self, db: AsyncSession):
        self.repository = ParentRepository(db)

    async def create_parent(self, parent_data: ParentCreate) -> Parent:
        parent = Parent(
            user_id=parent_data.user_id,
            first_name=parent_data.first_name,
            last_name=parent_data.last_name,
            relationship=parent_data.relationship,
            phone=parent_data.phone,
            email=str(parent_data.email) if parent_data.email else None,
            address=parent_data.address,
        )
        return await self.repository.create(parent)

    async def get_parent_by_id(self, parent_id: int) -> Parent:
        parent = await self.repository.get_by_id(parent_id)
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent not found",
            )
        return parent

    async def get_parents(
        self,
        page: int = 1,
        page_size: int = 10,
        is_active: bool | None = None,
    ) -> ParentListResponse:
        offset = (page - 1) * page_size
        total = await self.repository.count(is_active=is_active)
        items = await self.repository.get_paginated(
            offset=offset,
            limit=page_size,
            is_active=is_active,
        )
        pages = math.ceil(total / page_size) if total > 0 else 0

        return ParentListResponse(
            items=[ParentResponse.model_validate(p) for p in items],
            page=page,
            page_size=page_size,
            total=total,
            pages=pages,
        )

    async def update_parent(
        self,
        parent_id: int,
        update_data: ParentUpdate,
    ) -> Parent:
        parent = await self.get_parent_by_id(parent_id)
        data = update_data.model_dump(exclude_unset=True)
        if not data:
            return parent

        if "email" in data and data["email"] is not None:
            data["email"] = str(data["email"])

        return await self.repository.update(parent, data)

    async def deactivate_parent(self, parent_id: int) -> dict:
        parent = await self.get_parent_by_id(parent_id)
        await self.repository.delete(parent)
        return {
            "message": f"Parent '{parent.first_name} {parent.last_name}' deactivated successfully",
            "parent_id": parent_id,
        }
