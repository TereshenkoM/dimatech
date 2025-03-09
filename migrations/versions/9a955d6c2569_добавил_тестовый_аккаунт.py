"""Добавил тестовый аккаунт

Revision ID: 9a955d6c2569
Revises: acd019ebc75b
Create Date: 2025-03-09 18:00:58.453210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision: str = '9a955d6c2569'
down_revision: Union[str, None] = 'acd019ebc75b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    user_id = conn.execute(
        sa.text("SELECT id FROM public.user WHERE email = 'test@example.com'")
    ).scalar()

    if not user_id:
        raise ValueError("Тестовый пользователь не найден!")

    account_table = sa.table(
        'account',
        sa.Column('id', UUID(as_uuid=True)),
        sa.Column('balance', sa.Integer),
        sa.Column('user_id', UUID(as_uuid=True)),
        sa.Column('account_id', sa.String),
        sa.Column('created_at', sa.DateTime)
    )

    op.bulk_insert(account_table, [{
        'id': uuid.uuid4(),
        'balance': 1000,
        'user_id': user_id,
        'account_id': 'fas-ssa-ddd',
        'created_at': datetime.utcnow() 
    }])