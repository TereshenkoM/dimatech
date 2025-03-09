"""Добавил тестовый счёт

Revision ID: a97a9991ed3f
Revises: 86636d16080c
Create Date: 2025-03-09 12:56:41.105003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime



# revision identifiers, used by Alembic.
revision: str = 'a97a9991ed3f'
down_revision: Union[str, None] = '86636d16080c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Получаем connection для выполнения сырых SQL-запросов
    conn = op.get_bind()
    
    # Находим ID тестового пользователя по email
    user_id = conn.execute(
        sa.text("SELECT id FROM public.user WHERE email = 'test@example.com'")
    ).scalar()

    if not user_id:
        raise ValueError("Тестовый пользователь не найден!")

    # Создаем тестовый счет
    account_table = sa.table(
        'account',
        sa.Column('id', UUID(as_uuid=True)),
        sa.Column('balance', sa.Integer),
        sa.Column('user_id', UUID(as_uuid=True)),
        sa.Column('created_at', sa.DateTime)
    )

    op.bulk_insert(account_table, [{
        'id': uuid.uuid4(),
        'balance': 1000,  # Начальный баланс
        'user_id': user_id,
        'created_at': datetime.utcnow()
    }])

def downgrade():
    # Удаляем тестовый счет
    conn = op.get_bind()
    user_id = conn.execute(
        sa.text("SELECT id FROM public.user WHERE email = 'test@example.com'")
    ).scalar()
    
    if user_id:
        op.execute(
            sa.text("DELETE FROM account WHERE user_id = :user_id"),
            {'user_id': user_id}
        )