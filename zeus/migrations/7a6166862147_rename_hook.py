"""rename_hook

Revision ID: 7a6166862147
Revises: 4235d2fae82a
Create Date: 2017-07-11 14:16:37.282059

"""
import zeus
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7a6166862147'
down_revision = '4235d2fae82a'
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'hook',
        sa.Column('id', zeus.db.types.guid.GUID(), nullable=False),
        sa.Column('token', sa.LargeBinary(length=64), nullable=False),
        sa.Column('provider', sa.String(length=64), nullable=False),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('repository_id', zeus.db.types.guid.GUID(), nullable=False),
        sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_hook_repository_id'), 'hook', ['repository_id'], unique=False)
    op.drop_table('hook_token')
    op.drop_constraint('unq_job_provider', 'job', type_='unique')
    op.create_unique_constraint('unq_job_provider', 'job', ['build_id', 'provider', 'external_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unq_job_provider', 'job', type_='unique')
    op.create_unique_constraint(
        'unq_job_provider', 'job', ['repository_id', 'provider', 'external_id']
    )
    op.create_table(
        'hook_token',
        sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column('token', postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column('repository_id', postgresql.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['repository_id'], ['repository.id'],
            name='hook_token_repository_id_fkey',
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name='hook_token_pkey'),
        sa.UniqueConstraint('token', name='hook_token_token_key')
    )
    op.drop_index(op.f('ix_hook_repository_id'), table_name='hook')
    op.drop_table('hook')
    # ### end Alembic commands ###
