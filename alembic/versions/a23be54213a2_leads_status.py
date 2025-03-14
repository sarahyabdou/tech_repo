"""leads status

Revision ID: a23be54213a2
Revises: cc01ce708ef6
Create Date: 2025-03-12 03:35:45.610312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a23be54213a2'
down_revision: Union[str, None] = 'cc01ce708ef6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leads_stage',
    sa.Column('company_domain', sa.String(length=100), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lead_stage', sa.String(length=50), nullable=True),
    sa.Column('date_added', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_assigned', sa.Boolean(), nullable=True),
    sa.Column('is_not_assigned', sa.Boolean(), nullable=True),
    sa.Column('is_action_taken', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], ),
    sa.PrimaryKeyConstraint('company_domain', 'id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leads_stage')
    # ### end Alembic commands ###
