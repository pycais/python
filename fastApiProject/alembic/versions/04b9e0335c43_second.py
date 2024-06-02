"""second

Revision ID: 04b9e0335c43
Revises: a1c987230d59
Create Date: 2024-06-01 16:26:34.792906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04b9e0335c43'
down_revision: Union[str, None] = 'a1c987230d59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
