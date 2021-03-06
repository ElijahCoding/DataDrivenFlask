"""add product price and image

Revision ID: f4456eced18a
Revises: 69d1c22e0bc0
Create Date: 2020-06-04 17:21:04.126281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4456eced18a'
down_revision = '69d1c22e0bc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_url', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('price_cents', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('price_cents')
        batch_op.drop_column('picture_url')

    # ### end Alembic commands ###
