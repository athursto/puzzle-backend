"""empty message

Revision ID: 8eccb164156b
Revises: 7550099f1145
Create Date: 2020-09-21 20:30:17.645898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8eccb164156b'
down_revision = '7550099f1145'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('puzzle_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order', 'puzzle', ['puzzle_id'], ['id'])
    op.drop_constraint('puzzle_ibfk_1', 'puzzle', type_='foreignkey')
    op.drop_constraint('puzzle_ibfk_3', 'puzzle', type_='foreignkey')
    op.drop_constraint('puzzle_ibfk_2', 'puzzle', type_='foreignkey')
    op.drop_column('puzzle', 'owner_id')
    op.drop_column('puzzle', 'order_id')
    op.drop_column('puzzle', 'borrower_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('puzzle', sa.Column('borrower_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('puzzle', sa.Column('order_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('puzzle', sa.Column('owner_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('puzzle_ibfk_2', 'puzzle', 'order', ['order_id'], ['id'])
    op.create_foreign_key('puzzle_ibfk_3', 'puzzle', 'user', ['owner_id'], ['id'])
    op.create_foreign_key('puzzle_ibfk_1', 'puzzle', 'user', ['borrower_id'], ['id'])
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'puzzle_id')
    # ### end Alembic commands ###
