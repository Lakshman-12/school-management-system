import asyncio
from getpass import getpass

from sqlalchemy import select

from app.db.session import AsyncSessionLocal, engine
from app.core.security import hash_password
from app.modules.auth.models import User, UserRole


async def seed_admin() -> None:
    email = input("Enter admin email: ").strip().lower()
    password = getpass("Enter admin password: ")

    if not email or not password:
        print("Email and password are required.")
        return

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("A user with this email already exists.")
            return

        admin = User(
            email=email,
            password_hash=hash_password(password),
            role=UserRole.ADMIN,
            is_active=True,
        )

        db.add(admin)
        await db.commit()
        await db.refresh(admin)

        print(f"Admin created successfully. User ID: {admin.id}")


async def main() -> None:
    try:
        await seed_admin()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())