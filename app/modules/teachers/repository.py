from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.teachers.models import Teacher


class TeacherRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> Teacher | None:
        result = await self.db.execute(
            select(Teacher).where(
                Teacher.user_id == user_id
            )
        )

        return result.scalar_one_or_none()
    
    
    
    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()



    async def create_with_user(
        self,
        user: User,
        teacher: Teacher,
    ) -> Teacher:
        try:
            self.db.add(user)

            # Generate user.id before creating the teacher profile
            await self.db.flush()

            teacher.user_id = user.id
            self.db.add(teacher)

            await self.db.commit()

            await self.db.refresh(user)
            await self.db.refresh(teacher)

            return teacher

        except Exception:
            await self.db.rollback()
            raise
        
        
    
    async def get_all(self) -> list[Teacher]:
        result = await self.db.execute(
            select(Teacher).order_by(Teacher.id)
        )
        return list(result.scalars().all())
        
        
        
    async def get_by_id(
        self,
        teacher_id: int,
    ) -> Teacher | None:
        result = await self.db.execute(
            select(Teacher).where(
                Teacher.id == teacher_id
            )
        )
        return result.scalar_one_or_none()
    
    
    
    
    async def update(
        self,
        teacher: Teacher,
        update_data: dict,
    ) -> Teacher:
        try:
            for field, value in update_data.items():
                setattr(teacher, field, value)

            await self.db.commit()
            await self.db.refresh(teacher)

            return teacher

        except Exception:
            await self.db.rollback()
            raise
            
        
        
    @staticmethod
    async def count_teachers(
        db: AsyncSession,
    ) -> int:
        result = await db.execute(
            select(func.count(Teacher.id))
        )

        return result.scalar_one()



    @staticmethod
    async def get_teachers(
        db: AsyncSession,
        offset: int,
        limit: int,
    ) -> list[Teacher]:
        result = await db.execute(
            select(Teacher)
            .order_by(Teacher.id)
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def deactivate(self, teacher: Teacher) -> None:
        try:
            user = await self.get_user_by_id(teacher.user_id)
            if user:
                user.is_active = False
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

