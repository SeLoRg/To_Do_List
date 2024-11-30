"""Update tasks

Revision ID: a313b9d2e2fd
Revises: 5face81bee4e
Create Date: 2024-11-28 22:54:43.673013

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a313b9d2e2fd"
down_revision: Union[str, None] = "5face81bee4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Todoes")
    op.execute("DROP TYPE IF EXISTS status;")
    op.create_table(
        "Tasks",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("completed", "unfinished", name="status"),
            server_default="unfinished",
            nullable=False,
        ),
        sa.Column("data", sa.Date(), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["Users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Todoes",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM("completed", "unfinished", name="status"),
            server_default=sa.text("'unfinished'::status"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["Users.id"], name="Todoes_user_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="Todoes_pkey"),
    )
    op.drop_table("Tasks")
    # ### end Alembic commands ###
