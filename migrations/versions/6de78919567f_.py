"""empty message

Revision ID: 6de78919567f
Revises: 
Create Date: 2020-12-19 16:48:47.390365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6de78919567f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('time_start', sa.String(), nullable=True),
    sa.Column('time_end', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('user_type', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('user_token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('presences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('class_code', sa.String(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('token_expire', sa.Float(), nullable=True),
    sa.Column('presence', sa.Boolean(), nullable=True),
    sa.Column('num_classes', sa.Integer(), nullable=True),
    sa.Column('date', sa.Float(), nullable=True),
    sa.Column('confirmation_date', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('professor_class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('professor_id', sa.Integer(), nullable=True),
    sa.Column('class_code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_code'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['professor_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('class_code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_code'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_class')
    op.drop_table('professor_class')
    op.drop_table('presences')
    op.drop_table('users')
    op.drop_table('classes')
    # ### end Alembic commands ###
