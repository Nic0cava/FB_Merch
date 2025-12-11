"""Add FOH, BOH, Room300 qty columns and item_cost

Revision ID: ea1fa6dea662
Revises: 8b8f437eb387
Create Date: 2025-12-11 13:09:33.702105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea1fa6dea662'
down_revision = '8b8f437eb387'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns as nullable first so existing rows can be backfilled
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('foh_qty', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('boh_qty', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('room_300_qty', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('item_cost', sa.Float(), nullable=True))
        batch_op.drop_column('quantity')

    # Backfill NULLs on existing rows
    op.execute("UPDATE items SET foh_qty = 0 WHERE foh_qty IS NULL;")
    op.execute("UPDATE items SET boh_qty = 0 WHERE boh_qty IS NULL;")
    op.execute("UPDATE items SET room_300_qty = 0 WHERE room_300_qty IS NULL;")
    op.execute("UPDATE items SET item_cost = 0 WHERE item_cost IS NULL;")

    # Enforce NOT NULL and set server defaults
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('foh_qty', existing_type=sa.Integer(), nullable=False, server_default='0')
        batch_op.alter_column('boh_qty', existing_type=sa.Integer(), nullable=False, server_default='0')
        batch_op.alter_column('room_300_qty', existing_type=sa.Integer(), nullable=False, server_default='0')
        batch_op.alter_column('item_cost', existing_type=sa.Float(), nullable=False, server_default='0')


def downgrade():
    # Recreate legacy quantity column, backfill, then drop new fields
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=True))

    op.execute(
        "UPDATE items SET quantity = "
        "COALESCE(foh_qty, 0) + COALESCE(boh_qty, 0) + COALESCE(room_300_qty, 0) "
        "WHERE quantity IS NULL;"
    )

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('quantity', existing_type=sa.Integer(), nullable=False, server_default='0')
        batch_op.drop_column('item_cost')
        batch_op.drop_column('room_300_qty')
        batch_op.drop_column('boh_qty')
        batch_op.drop_column('foh_qty')
