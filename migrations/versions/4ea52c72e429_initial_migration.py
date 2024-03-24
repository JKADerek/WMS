"""Initial migration

Revision ID: 4ea52c72e429
Revises: d7ea03e69efe
Create Date: 2024-03-24 17:11:43.897762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ea52c72e429'
down_revision = 'd7ea03e69efe'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=100), nullable=False),
    sa.Column('sku', sa.String(length=20), nullable=False),
    sa.Column('quantity_in_stock', sa.Integer(), nullable=False),
    sa.Column('reorder_level', sa.Integer(), nullable=False),
    sa.Column('unit_cost', sa.Float(), nullable=False),
    sa.Column('supplier_name', sa.String(length=100), nullable=False),
    sa.Column('supplier_contact', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('image_filename', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_inventory_item'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('must_reset_password', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_user_role_id_role')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email'))
    )
    # ### end Alembic commands ###