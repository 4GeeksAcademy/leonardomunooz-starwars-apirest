"""empty message

Revision ID: 6839a176285a
Revises: 45a71e915b47
Create Date: 2024-11-01 19:32:50.293029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6839a176285a'
down_revision = '45a71e915b47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('favorite_people_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorite_people_id_fkey', 'user', ['people_id'], ['id'])
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
