"""Seed migration

Revision ID: b696a6ffe127
Revises:
Create Date: 2022-10-15 13:23:47.172672

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from used_stuff_market.db.tsvector import TSVector

# revision identifiers, used by Alembic.
revision = "b696a6ffe127"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS availability")
    op.execute("CREATE SCHEMA IF NOT EXISTS catalog")
    op.execute("CREATE SCHEMA IF NOT EXISTS items")
    op.create_table(
        "resources",
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", postgresql.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("locked_by", postgresql.UUID(), nullable=True),
        sa.Column("locked_to", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("uuid"),
        schema="availability",
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "ts_vector",
            TSVector(),
            sa.Computed(
                (
                    "to_tsvector('english', COALESCE(data->>'title', '') || "
                    "' ' || COALESCE(data->>'description', ''))"
                ),
                persisted=True,
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="catalog",
    )
    op.create_index(
        "ix_ts_vector",
        "products",
        ["ts_vector"],
        unique=False,
        schema="catalog",
        postgresql_using="gin",
    )
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("starting_price_amount", sa.Numeric(), nullable=True),
        sa.Column("starting_price_currency", sa.String(length=3), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="items",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("items", schema="items")
    op.drop_index(
        "ix_ts_vector",
        table_name="products",
        schema="catalog",
        postgresql_using="gin",
    )
    op.drop_table("products", schema="catalog")
    op.drop_table("resources", schema="availability")
    # ### end Alembic commands ###
