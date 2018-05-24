"""empty message

Revision ID: 045c34489f55
Revises: 
Create Date: 2018-05-25 00:32:28.577000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '045c34489f55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('texts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('textname', sa.Text(), nullable=True),
    sa.Column('nrtokens', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('textname')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('auth_provider', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('family_name', sa.String(length=60), nullable=True),
    sa.Column('picture_url', sa.String(length=128), nullable=True),
    sa.Column('access_level', sa.Integer(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_family_name'), 'users', ['family_name'], unique=False)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_picture_url'), 'users', ['picture_url'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('exo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('textid', sa.Integer(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('exotoknum', sa.Integer(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['textid'], ['texts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sentences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text_id', sa.Integer(), nullable=True),
    sa.Column('nr', sa.Integer(), nullable=True),
    sa.Column('sentence', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['text_id'], ['texts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sentencesearch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nr', sa.Integer(), nullable=True),
    sa.Column('sentence', sa.Text(), nullable=True),
    sa.Column('textid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['textid'], ['texts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('textid', sa.Integer(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['textid'], ['texts.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sentencefeatures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sentenceid', sa.Integer(), nullable=False),
    sa.Column('attr', sa.Text(), nullable=True),
    sa.Column('value', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['sentenceid'], ['sentences.id'], ),
    sa.PrimaryKeyConstraint('id', 'sentenceid')
    )
    op.create_table('trees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sentenceid', sa.Integer(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sentenceid'], ['sentences.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('treeid', sa.Integer(), nullable=True),
    sa.Column('nr', sa.Integer(), nullable=False),
    sa.Column('attr', sa.Text(), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['treeid'], ['trees.id'], ),
    sa.PrimaryKeyConstraint('id', 'nr', 'attr')
    )
    op.create_table('links',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('treeid', sa.Integer(), nullable=True),
    sa.Column('depid', sa.Integer(), nullable=True),
    sa.Column('govid', sa.Integer(), nullable=True),
    sa.Column('function', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['treeid'], ['trees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('links')
    op.drop_table('features')
    op.drop_table('trees')
    op.drop_table('sentencefeatures')
    op.drop_table('todos')
    op.drop_table('sentencesearch')
    op.drop_table('sentences')
    op.drop_table('exo')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_picture_url'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_family_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('texts')
    op.drop_table('projects')
    # ### end Alembic commands ###