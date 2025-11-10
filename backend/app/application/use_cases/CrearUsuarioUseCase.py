"""
Caso de Uso: Crear un nuevo Usuario (Docente).

Este archivo contiene la lógica de negocio pura para
registrar un nuevo docente en el sistema.
"""

# DTOs de Dominio
from app.domain.entities.usuario import Usuario, UsuarioCreate
# Interfaz de Dominio
from app.domain.repositories.usuario_repository import IUsuarioRepository
# Excepciones y Seguridad del Core
from app.core.exceptions import AlreadyExistsException


class CrearUsuarioUseCase:
    """
    Clase que encapsula la lógica para crear un usuario.
    Sigue el patrón de Caso de Uso (Use Case).
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        """
        Inicializa el caso de uso con sus dependencias (inyectadas).

        Args:
            usuario_repository: Implementación de la interfaz IUsuarioRepository.
        """
        self.usuario_repository = usuario_repository

    async def execute(self, usuario_create: UsuarioCreate) -> Usuario:
        """
        Ejecuta la lógica del caso de uso.

        Args:
            usuario_create: DTO con los datos del nuevo usuario.

        Raises:
            AlreadyExistsException: Si el email ya está registrado.

        Returns:
            La entidad Usuario recién creada.
        """
        # 1. Verificar si el email ya existe (regla de negocio)
        existing_user = await self.usuario_repository.get_by_email(usuario_create.email)
        if existing_user:
            raise AlreadyExistsException(
                resource="Usuario", field="email", value=usuario_create.email
            )

        # 2. Crear el usuario en la base de datos
        #    El repositorio se encarga de la lógica de la DB, incluido el hasheo.
        nuevo_usuario = await self.usuario_repository.create(usuario_create)

        # 3. Retornar la entidad creada
        return nuevo_usuario

