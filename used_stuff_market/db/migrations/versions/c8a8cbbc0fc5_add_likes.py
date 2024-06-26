"""Add likes

Revision ID: c8a8cbbc0fc5
Revises: 5606eebf14c9
Create Date: 2022-10-19 12:37:27.461966

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c8a8cbbc0fc5"
down_revision = "5606eebf14c9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA likes")
    op.create_table(
        "likes",
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("liker", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("item_id", "liker"),
        schema="likes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("likes", schema="likes")
    # ### end Alembic commands ###
