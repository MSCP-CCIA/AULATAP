import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- INICIO DE LA MODIFICACIÓN ---
# add your model's MetaData object here
# for 'autogenerate' support

# 1. Añade el directorio 'backend' (padre de 'alembic') al path de Python.
backend_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)

# 2. Importa el PAQUETE de modelos (esto ejecuta __init__.py)
import app.infrastructure.persistence.models

# 3. Importa la clase 'Base' desde su ubicación exacta
from app.infrastructure.persistence.models.base import Base

# 4. Asigna la metadata de tu Base al target_metadata
target_metadata = Base.metadata

# --- FIN DE LA MODIFICACIÓN ---


# other values from the config, defined by the needs of .env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    ...
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    ...
    """
    connectable = engine_from_config(
        # ESTA ES LA CORRECCIÓN FINAL
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()