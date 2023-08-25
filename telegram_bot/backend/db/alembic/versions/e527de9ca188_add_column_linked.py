"""add_column_linked

Revision ID: e527de9ca188
Revises: ec0491c08e5e
Create Date: 2023-08-17 14:35:04.445922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e527de9ca188"
down_revision: Union[str, None] = "ec0491c08e5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("linked", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "linked")
    # ### end Alembic commands ###