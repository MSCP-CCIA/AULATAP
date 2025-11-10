"""
Paquete de Repositorios de Persistencia (Implementaciones)

Exporta las implementaciones concretas de los repositorios.
"""

from .usuario_repository_impl import UsuarioRepositoryImpl
from .estudiante_repository_impl import EstudianteRepositoryImpl
from .horario_repository_impl import HorarioRepositoryImpl
from .asignatura_repository_impl import AsignaturaRepositoryImpl
from .sesion_de_clase_repository_impl import SesionDeClaseRepositoryImpl
from .registro_asistencia_repository_impl import RegistroAsistenciaRepositoryImpl
from .inscripcion_repository_impl import InscripcionRepositoryImpl
from .clase_programada_repository_impl import ClaseProgramadaRepositoryImpl

__all__ = [
    "UsuarioRepositoryImpl",
    "EstudianteRepositoryImpl",
    "HorarioRepositoryImpl",
    "AsignaturaRepositoryImpl",
    "SesionDeClaseRepositoryImpl",
    "RegistroAsistenciaRepositoryImpl",
    "InscripcionRepositoryImpl",
    "ClaseProgramadaRepositoryImpl",
]
