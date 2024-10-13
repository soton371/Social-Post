"""add content colum to posts table

Revision ID: 257574240a34
Revises: c285645d9c3c
Create Date: 2024-10-13 19:03:27.647725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '257574240a34'
down_revision: Union[str, None] = 'c285645d9c3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String()))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass

