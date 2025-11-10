import asyncio
import os
import sys
import platform

# --- Path Setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# --- Windows + psycopg fix ---
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.core.database import get_db
from app.domain.entities.usuario import UsuarioCreate
from app.application.use_cases.CrearUsuarioUseCase import CrearUsuarioUseCase
from app.infrastructure.persistence.repositories.usuario_repository_impl import UsuarioRepositoryImpl

async def main():
    print("Creating a new user...")
    db_session_generator = get_db()
    db = await anext(db_session_generator)
    try:
        repo = UsuarioRepositoryImpl(db)
        use_case = CrearUsuarioUseCase(repo)

        user_to_create = UsuarioCreate(
            email="test@example.com",
            nombre_completo="Test User",
            password="password123"
        )

        new_user = await use_case.execute(user_to_create)
        print("User created successfully:")
        print(f"  ID: {new_user.id}")
        print(f"  Email: {new_user.email}")
        print(f"  Nombre: {new_user.nombre_completo}")

    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
