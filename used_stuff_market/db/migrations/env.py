# flake8: noqa
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

# for model discovery
from used_stuff_market.availability.models import Resource
from used_stuff_market.catalog.models import Product
from used_stuff_market.db import Base, DbSettings
from used_stuff_market.items_infrastructure.models import items
from used_stuff_market.likes.models import Like
from used_stuff_market.payments.models import Payment
from used_stuff_market.processes.buying.models import *
from used_stuff_market.users.models import User

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  # type: ignore


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DbSettings().URL
    context.configure(
        url=str(url),
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(str(DbSettings().URL), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
