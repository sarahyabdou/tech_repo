"""user roles

Revision ID: 7ddc83b371d9
Revises: d234420566b7
Create Date: 2025-03-12 02:34:44.380037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ddc83b371d9'
down_revision: Union[str, None] = 'd234420566b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_domain', sa.String(length=100), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['company_domain'], ['company_info.company_domain'], ),
    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company_domain', 'module_id', 'name', name='uq_user_roles')
    )
    op.create_table('user_role_mapping',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['user_roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.create_table('user_role_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('module_id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=False),
    sa.Column('d_read', sa.Boolean(), nullable=True),
    sa.Column('d_write', sa.Boolean(), nullable=True),
    sa.Column('d_edit', sa.Boolean(), nullable=True),
    sa.Column('d_delete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['module_id', 'feature_id'], ['module_features.module_id', 'module_features.feature_id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['user_roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role_permissions')
    op.drop_table('user_role_mapping')
    op.drop_table('user_roles')
    # ### end Alembic commands ###
