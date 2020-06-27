"""empty message

Revision ID: a345a0e534fc
Revises: 
Create Date: 2020-06-27 23:35:36.712756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a345a0e534fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('about',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_name', sa.String(length=64), nullable=False),
    sa.Column('img1', sa.String(length=64), nullable=False),
    sa.Column('img2', sa.String(length=64), nullable=False),
    sa.Column('img3', sa.String(length=64), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('avator', sa.String(length=64), nullable=True),
    sa.Column('create_time', sa.String(length=32), nullable=False),
    sa.Column('login_time', sa.String(length=32), nullable=True),
    sa.Column('superuser', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('price', sa.String(length=32), nullable=False),
    sa.Column('img', sa.String(length=64), nullable=True),
    sa.Column('detail_info', sa.Text(), nullable=True),
    sa.Column('view_num', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statistics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ip_addr', sa.String(length=64), nullable=False),
    sa.Column('create_time', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('visit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('visit_num', sa.Integer(), nullable=True),
    sa.Column('clean_time', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('contact', sa.String(length=64), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('objective_item', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['objective_item'], ['item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    op.drop_table('visit')
    op.drop_table('statistics')
    op.drop_table('item')
    op.drop_table('admin')
    op.drop_table('about')
    # ### end Alembic commands ###
