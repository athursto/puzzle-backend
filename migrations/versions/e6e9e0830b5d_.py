"""empty message

Revision ID: e6e9e0830b5d
Revises: 14d052828c9c
Create Date: 2020-09-11 02:14:39.797603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6e9e0830b5d'
down_revision = '14d052828c9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('puzzle', sa.Column('name_of_puzzle', sa.String(length=50), nullable=False))
    op.add_column('puzzle', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'puzzle', ['name_of_puzzle'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'puzzle', type_='unique')
    op.drop_column('puzzle', 'owner_id')
    op.drop_column('puzzle', 'name_of_puzzle')
    # ### end Alembic commands ###