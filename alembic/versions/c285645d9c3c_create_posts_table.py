"""create posts table

Revision ID: c285645d9c3c
Revises: 
Create Date: 2024-10-13 15:48:08.182294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c285645d9c3c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(
    ), nullable=False, primary_key=True), sa.Column('title', sa.String(),))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass


