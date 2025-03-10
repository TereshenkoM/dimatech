"""Добавил тестового пользователя

Revision ID: acd019ebc75b
Revises: 3dc8c6463af6
Create Date: 2025-03-09 17:58:57.325983

"""
import uuid
from datetime import datetime
from typing import Sequence, Union

import bcrypt
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'acd019ebc75b'
down_revision: Union[str, None] = '3dc8c6463af6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # Создаем объект таблицы для вставки
    user_table = sa.table(
        'user',
        sa.Column('id', UUID(as_uuid=True)),
        sa.Column('email', sa.String),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('father_name', sa.String),
        sa.Column('password', sa.String),
        sa.Column('is_active', sa.Boolean),
        sa.Column('is_staff', sa.Boolean),
        sa.Column('is_super_user', sa.Boolean),
        sa.Column('created_at', sa.DateTime)
    )

    # Данные для тестового пользователя и администратора
    users = [
        {
            'id': uuid.uuid4(),
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'father_name': 'Testovich',
            'password': bcrypt.hashpw('testpassword'.encode(), bcrypt.gensalt()).decode(),
            'is_active': True,
            'is_staff': False,
            'is_super_user': False,
            'created_at': datetime.utcnow()
        },
        {
            'id': uuid.uuid4(),
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'father_name': 'Adminovich',
            'password': bcrypt.hashpw('adminpassword'.encode(), bcrypt.gensalt()).decode(),
            'is_active': True,
            'is_staff': True,
            'is_super_user': True,
            'created_at': datetime.utcnow()
        }
    ]

    # Вставляем данные
    op.bulk_insert(user_table, users)

def downgrade():
    # Удаляем добавленных пользователей по email
    op.execute(
        "DELETE FROM user WHERE email IN ('test@example.com', 'admin@example.com')"
    )