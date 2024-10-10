from __future__ import print_function
import logging
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

load_dotenv()

config = context.config

config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

logger = logging.getLogger('alembic.runtime.migration')
logger.setLevel(logging.INFO)

target_metadata = None

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise RuntimeError("Offline mode is not supported")
else:
    run_migrations_online()
