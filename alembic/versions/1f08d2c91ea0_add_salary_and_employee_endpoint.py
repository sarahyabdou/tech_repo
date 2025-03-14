"""add salary and employee endpoint 

Revision ID: 1f08d2c91ea0
Revises: 18672fa4c54c
Create Date: 2025-03-13 21:58:15.011175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f08d2c91ea0'
down_revision: Union[str, None] = '18672fa4c54c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'employees_info', ['user_uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employees_info', type_='unique')
    # ### end Alembic commands ###
