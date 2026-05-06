from logging.config import fileConfig
import os
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Import your SQLAlchemy Base
from app.db.base import Base

# ---------------------------------
# LOAD ROOT .ENV
# ---------------------------------
load_dotenv("../.env")

# ---------------------------------
# ALEMBIC CONFIG
# ---------------------------------
config = context.config

# ---------------------------------
# DATABASE CONFIG
# ---------------------------------
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

encoded_password = quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"postgresql://{DB_USER}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Inject DB URL into Alembic
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL.replace("%", "%%")
)

# ---------------------------------
# LOGGING
# ---------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------
# SQLALCHEMY METADATA
# ---------------------------------
target_metadata = Base.metadata


# ---------------------------------
# OFFLINE MIGRATIONS
# ---------------------------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------
# ONLINE MIGRATIONS
# ---------------------------------
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------
# RUN
# ---------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
