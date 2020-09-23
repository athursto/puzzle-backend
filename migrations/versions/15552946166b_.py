"""empty message

Revision ID: 15552946166b
Revises: 8ecde7fc5654
Create Date: 2020-09-19 14:44:59.081575

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '15552946166b'
down_revision = '8ecde7fc5654'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('puzzle', 'borrower_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('puzzle', 'borrower_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###