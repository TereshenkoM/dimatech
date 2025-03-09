"""Удалил лишнее поле

Revision ID: 5430013c0538
Revises: 9a955d6c2569
Create Date: 2025-03-09 18:14:53.428554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5430013c0538'
down_revision: Union[str, None] = '9a955d6c2569'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'signature')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('signature', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
