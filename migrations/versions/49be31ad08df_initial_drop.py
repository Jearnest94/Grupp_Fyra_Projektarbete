"""Initial drop

Revision ID: 49be31ad08df
Revises: 
Create Date: 2022-01-18 23:59:34.828507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49be31ad08df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('mangocount', sa.Integer(), nullable=True),
    sa.Column('admin', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('messages',
    sa.Column('messageid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fromuser', sa.BigInteger(), nullable=False),
    sa.Column('touser', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('content', sa.String(length=250), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['fromuser'], ['user.id'], ),
    sa.ForeignKeyConstraint(['touser'], ['user.id'], ),
    sa.PrimaryKeyConstraint('messageid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('user')
    # ### end Alembic commands ###