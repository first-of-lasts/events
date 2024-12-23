"""init

Revision ID: 133f8e6c7a8e
Revises: 
Create Date: 2024-12-22 13:47:50.762795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '133f8e6c7a8e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('name_ru', sa.String(length=255), nullable=True),
    sa.Column('name_uz', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('bio', sa.String(length=2048), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index('idx_users_country_id', 'users', ['country_id'], unique=False)
    op.create_table('events',
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=2048), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['organizer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    op.drop_index('idx_users_country_id', table_name='users')
    op.drop_table('users')
    op.drop_table('countries')
    # ### end Alembic commands ###
