"""Обновил модель UserORM

Revision ID: b54e9f697fe2
Revises: ce43d1c40fd6
Create Date: 2025-03-09 12:06:08.975214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b54e9f697fe2'
down_revision: Union[str, None] = 'ce43d1c40fd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(), nullable=False))
    op.add_column('user', sa.Column('last_name', sa.String(), nullable=False))
    op.add_column('user', sa.Column('father_name', sa.String(), nullable=False))
    op.add_column('user', sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now()::timestamp)"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'created_at')
    op.drop_column('user', 'father_name')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
