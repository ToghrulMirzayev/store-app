"""address column added to the stores table

Revision ID: 480b1e0263f7
Revises: 
Create Date: 2024-01-08 01:01:48.193169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '480b1e0263f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stores', sa.Column('address', sa.String(), default=None))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('id', sa.Integer(), primary_key=True, index=True))
    op.add_column('users', sa.Column('email', sa.String(), unique=True))
    op.add_column('users', sa.Column('username', sa.String(), unique=True))
    op.add_column('users', sa.Column('first_name', sa.String()))
    op.add_column('users', sa.Column('last_name', sa.String()))
    op.add_column('users', sa.Column('hashed_password', sa.String()))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), default=True))
    op.add_column('users', sa.Column('role', sa.String()))

    op.add_column('stores', sa.Column('store_id', sa.Integer(), primary_key=True, index=True, autoincrement=True))
    op.add_column('stores', sa.Column('store_name', sa.String(), index=True))
    op.add_column('stores', sa.Column('location', sa.String()))

    op.add_column('products', sa.Column('product_id', sa.Integer(), primary_key=True, index=True, autoincrement=True))
    op.add_column('products', sa.Column('product_name', sa.String(), index=True))
    op.add_column('products', sa.Column('is_available', sa.Boolean(), default=True))
    op.add_column('products', sa.Column('store_id', sa.Integer()))
    op.create_foreign_key('products_store_id_fkey', 'products', 'stores', ['store_id'], ['store_id'])
    # ### end Alembic commands ###