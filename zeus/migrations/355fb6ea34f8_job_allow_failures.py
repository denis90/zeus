"""job_allow_failures

Revision ID: 355fb6ea34f8
Revises: 53c5cd5b170f
Create Date: 2017-09-29 13:27:31.861345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '355fb6ea34f8'
down_revision = '53c5cd5b170f'
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'job',
        sa.Column(
            'allow_failure',
            sa.Boolean(),
            server_default='0',
            nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job', 'allow_failure')
    # ### end Alembic commands ###
