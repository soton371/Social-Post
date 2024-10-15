"""add last few columns to posts table

Revision ID: 9f392a94f59b
Revises: a2d41404e63b
Create Date: 2024-10-15 21:06:54.362313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f392a94f59b'
down_revision: Union[str, None] = 'a2d41404e63b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass



