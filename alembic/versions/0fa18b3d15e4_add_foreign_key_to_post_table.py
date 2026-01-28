"""add foreign key to post table

Revision ID: 0fa18b3d15e4
Revises: 3487ab59e499
Create Date: 2026-01-28 22:51:14.819677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fa18b3d15e4'
down_revision: Union[str, Sequence[str], None] = '3487ab59e499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.UUID(as_uuid=True), nullable=False),
        schema='course_jwt'
        )
    op.create_foreign_key(
        constraint_name='posts_owner_id_fkey',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        source_schema='course_jwt',
        referent_schema='course_jwt',
        ondelete='CASCADE'
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        constraint_name='posts_owner_id_fkey',
        table_name='posts',
        schema='course_jwt',
        type_='foreignkey'
        )
    op.drop_column(
        table_name='posts',
        column_name='owner_id',
        schema='course_jwt'
        )
