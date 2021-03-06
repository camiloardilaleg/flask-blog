"""Add created field to Post

Revision ID: dd3a5245a8ea
Revises: 8cb5f8e304fc
Create Date: 2022-06-13 13:31:26.048336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd3a5245a8ea'
down_revision = '8cb5f8e304fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'created')
    # ### end Alembic commands ###
