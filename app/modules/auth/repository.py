from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User


class AuthRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        statement = select(User).where(
            User.email == email
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def create_user(
        self,
        email: str,
        password_hash: str,
    ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            role="student",
        )

        self.db.add(user)

        await self.db.flush()

        return user
    
    
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()