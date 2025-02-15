"""Update todoes

Revision ID: 5face81bee4e
Revises: 63315e0fd25f
Create Date: 2024-11-28 15:28:30.296489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5face81bee4e'
down_revision: Union[str, None] = '63315e0fd25f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Todoes', sa.Column('status', sa.Enum('completed', 'unfinished', name='status'), server_default='unfinished', nullable=False))
    op.alter_column('Todoes', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('Todoes', 'status_id')
    op.drop_column('Todoes', 'expiration_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Todoes', sa.Column('expiration_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('Todoes', sa.Column('status_id', postgresql.ENUM('completed', 'unfinished', name='status'), server_default=sa.text("'unfinished'::status"), autoincrement=False, nullable=False))
    op.alter_column('Todoes', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('Todoes', 'status')
    # ### end Alembic commands ###
