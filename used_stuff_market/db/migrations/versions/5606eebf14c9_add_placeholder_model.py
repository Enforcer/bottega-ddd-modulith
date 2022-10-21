"""Add placeholder model

Revision ID: 5606eebf14c9
Revises: 4d4800579e1e
Create Date: 2022-10-18 22:06:51.934135

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5606eebf14c9"
down_revision = "4d4800579e1e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "placeholder",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="processes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("placeholder", schema="processes")
    # ### end Alembic commands ###
