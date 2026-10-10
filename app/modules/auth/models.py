from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLAlchemyEnum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True,)

    email: Mapped[str] = mapped_column(String(255),unique=True,index=True,nullable=False,)

    password_hash: Mapped[str] = mapped_column(String(255),nullable=False,)

    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(
            UserRole,
            name="user_role",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )