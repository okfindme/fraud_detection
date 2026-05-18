"""increased the word limit in notes attribute of AuditLog class 

Revision ID: 7c95c0a8e1cd
Revises: a8aac4f624ec
Create Date: 2026-05-10 01:20:55.338171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c95c0a8e1cd'
down_revision: Union[str, Sequence[str], None] = 'a8aac4f624ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('audit_logs') as batch_op:
        batch_op.alter_column('notes',
            existing_type=sa.String(length=250),
            type_=sa.String(length=500),
            existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('audit_logs') as batch_op:
        batch_op.alter_column('notes',
            existing_type=sa.String(length=500),
            type_=sa.String(length=250),
            existing_nullable=True)
