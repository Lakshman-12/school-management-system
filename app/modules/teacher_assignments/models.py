from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TeacherAssignment(Base):
    __tablename__ = "teacher_assignments"

    __table_args__ = (
        UniqueConstraint(
            "teacher_id",
            "class_id",
            "subject_id",
            name="uq_teacher_class_subject",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"),
        nullable=False,
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey("school_classes.id"),
        nullable=False,
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False,
    )