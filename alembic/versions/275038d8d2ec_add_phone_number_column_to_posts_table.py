"""add phone number column to posts table

Revision ID: 275038d8d2ec
Revises: 68f6e362112f
Create Date: 2026-01-21 00:19:10.431352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '275038d8d2ec'
down_revision: Union[str, Sequence[str], None] = '68f6e362112f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('phone_number', sa.String(10), nullable=True),
        schema='course_jwt'
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'posts',
        'phone_number',
        schema='course_jwt'
        )
