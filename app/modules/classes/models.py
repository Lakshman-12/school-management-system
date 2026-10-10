from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SchoolClass(Base):
    __tablename__ = "school_classes"

    __table_args__ = (
        UniqueConstraint(
            "name",
            "section",
            "academic_year",
            name="uq_school_class_section_year",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    section: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    academic_year: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    
    
    
    
