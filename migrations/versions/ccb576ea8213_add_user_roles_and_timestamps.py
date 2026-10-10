"""add user roles and timestamps

Revision ID: ccb576ea8213
Revises: e4aae3e7bf9b
Create Date: 2026-09-30 15:15:44.282422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccb576ea8213'
down_revision: Union[str, Sequence[str], None] = 'e4aae3e7bf9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role = sa.Enum(
        "admin",
        "teacher",
        "student",
        "parent",
        name="user_role",
    )

    # Create the PostgreSQL enum type first.
    user_role.create(op.get_bind(), checkfirst=True)

    # Add the role column.
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
        ),
    )

    # Add timestamps.
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    op.drop_column("users", "role")

    user_role = sa.Enum(
        "admin",
        "teacher",
        "student",
        "parent",
        name="user_role",
    )

    user_role.drop(op.get_bind(), checkfirst=True)