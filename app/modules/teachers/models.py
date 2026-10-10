from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),unique=True,nullable=False,)
    full_name: Mapped[str] = mapped_column(String(100),nullable=False,)
    qualification: Mapped[str | None] = mapped_column(String(100),nullable=True,)
    phone: Mapped[str | None] = mapped_column(String(15),nullable=True,)
    
    
    