"""create parents and students tables

Revision ID: 3a8c1f9b7e42
Revises: 10887de34dae
Create Date: 2026-10-10 12:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a8c1f9b7e42'
down_revision: Union[str, Sequence[str], None] = '10887de34dae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create parents table
    op.create_table(
        'parents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('relationship', sa.String(length=50), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_parents_id'), 'parents', ['id'], unique=False)
    op.create_index(op.f('ix_parents_phone'), 'parents', ['phone'], unique=False)

    # 2. Create students table
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('admission_number', sa.String(length=50), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['class_id'], ['school_classes.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['parent_id'], ['parents.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False)
    op.create_index(op.f('ix_students_admission_number'), 'students', ['admission_number'], unique=True)
    op.create_index(op.f('ix_students_class_id'), 'students', ['class_id'], unique=False)
    op.create_index(op.f('ix_students_parent_id'), 'students', ['parent_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_students_parent_id'), table_name='students')
    op.drop_index(op.f('ix_students_class_id'), table_name='students')
    op.drop_index(op.f('ix_students_admission_number'), table_name='students')
    op.drop_index(op.f('ix_students_id'), table_name='students')
    op.drop_table('students')

    op.drop_index(op.f('ix_parents_phone'), table_name='parents')
    op.drop_index(op.f('ix_parents_id'), table_name='parents')
    op.drop_table('parents')
