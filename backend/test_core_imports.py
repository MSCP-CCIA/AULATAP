"""
Script para probar que todos los módulos del 'core' se importan
y configuran correctamente, incluyendo la conexión a la base de datos
y la carga del .env
"""

import asyncio
import os
import sys
import platform

# --- Configuración del Path ---
# Añadir la carpeta 'backend' al sys.path para que 'app...' funcione
# __file__ es .../backend/test_core_imports.py
# current_dir es .../backend
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"Añadido al path: {current_dir}\n")

# --- Arreglo para Windows + psycopg ---
# psycopg no es compatible con el ProactorEventLoop por defecto.
# Forzamos el SelectorEventLoop. Esto genera un DeprecationWarning
# en Python 3.14+, pero es REQUERIDO para que psycopg funcione.
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    print("Iniciando prueba de importación del Core...")
    logger = None  # Inicializar logger

    try:
        # 0. Probar el conflicto de 'logger'
        print("Importando SQLAlchemy (disparador de la prueba de 'logger')...")
        import sqlalchemy
        print("    -> OK. SQLAlchemy importado (no hay conflicto con 'logger').\n")

        # 1. Importar Config (Esto carga y valida el .env)
        print("1. Importando config...")
        from app.core.config import settings

        # Ahora que 'settings' está cargado, podemos obtener el logger
        from app.core.logger import get_logger
        logger = get_logger("aulatap")  # Obtener el logger principal

        print(f"    -> OK. Config cargada. APP_NAME: {settings.APP_NAME}")
        print(f"    -> OK. DEBUG: {settings.DEBUG}")

        # Ocultar contraseñas en el log
        db_url_safe = settings.DATABASE_URL.split('@')[0] if '@' in settings.DATABASE_URL else settings.DATABASE_URL
        db_sync_url_safe = settings.database_url_sync.split('@')[
            0] if '@' in settings.database_url_sync else settings.database_url_sync

        print(f"    -> OK. DATABASE_URL: {db_url_safe}@...")
        print(f"    -> URL Síncrona (Alembic): {db_url_safe}@...")

        # 2. Importar el resto del core
        print("\n2. Importando logger, security, exceptions...")
        from app.core.security import create_access_token, get_password_hash, verify_password
        from app.core.exceptions import register_exception_handlers
        logger.info("    -> OK. Logger de 'logger.py' funcionando.", extra={"test": "true"})
        print("    -> OK. Módulos (security, exceptions) importados.")

        # 3. Importar Database (Prueba de Base y Conexión)
        print("\n3. Importando database y probando conexión...")
        from app.core.database import get_db, engine, Base

        async with engine.connect() as conn:
            await conn.run_sync(lambda sync_conn: print("    -> OK. Conexión a DB exitosa."))

        # 4. Probar que la 'Base' (metadata) de Alembic se cargó
        print("\n4. Verificando metadata de SQLAlchemy (tablas de Alembic)...")
        tables = Base.metadata.tables.keys()

        # Convertir a minúsculas para comparación agnóstica
        tables_lower = {t.lower() for t in tables}

        if "usuario" in tables_lower:
            print(f"    -> OK. ¡Metadata cargada! Encontradas {len(tables)} tablas (ej: 'usuario').")
        else:
            print(f"    -> ¡ERROR! La 'Base' está vacía o es incorrecta. No se encontraron tablas de Alembic.")
            print(f"    -> Tablas encontradas: {tables}")
            print(f"    -> Asegúrate de que 'database.py' importa la Base desde 'app.infrastructure...'.")

        # 5. Probar hashing (corregido para 'argon2')
        print("\n5. Importando security (probando hash)...")
        password_plana = "test123"
        test_hash = get_password_hash(password_plana)
        print(f"    -> OK. Hash de prueba (argon2): {test_hash[:20]}...")  # Imprime solo el inicio

        # --- ESTA ES LA CORRECCIÓN ---
        # No comparamos el string, verificamos el hash.
        is_valid = verify_password(password_plana, test_hash)
        assert is_valid == True
        print("    -> OK. Assert de hash (argon2) superado.")

        # 6. Importar Dependencias (probando los mocks)
        print("\n6. Importando dependencies (con mocks)...")
        from app.core.dependencies import PermissionChecker, require_role
        print("    -> OK. Módulo de dependencias importado.\n")

        print("=" * 30)
        print("¡ÉXITO! Todo el módulo 'core' se importó y configuró correctamente.")
        print("=" * 30)

    except ImportError as e:
        print("\n--- ¡ERROR DE IMPORTACIÓN! ---")
        print(f"No se pudo importar: {e}")
        print("Asegúrate de que tus archivos __init__.py están en su sitio.")
        print("Si el error es sobre 'app.domain', es normal (ver 'dependencies.py')")

    except Exception as e:
        print("\n--- ¡ERROR! ---")
        print(f"Ocurrió un error durante la prueba: {e}")
        print("\nTraceback:")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Asegurarse de que el túnel SSH esté activo y .env esté en 'backend/'
    print("Recordatorio: Asegúrate de que tu túnel SSH esté activo y tu .env esté en la carpeta 'backend'.")
    asyncio.run(main())

