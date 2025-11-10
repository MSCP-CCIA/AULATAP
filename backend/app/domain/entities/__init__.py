"""
Paquete de Entidades de Dominio (DTOs)

Exporta las clases Pydantic que definen los objetos de negocio
y los contratos de datos (DTOs) entre capas.
"""
from .usuario import Usuario, UsuarioCreate, UsuarioPublic, UsuarioUpdate
from .estudiante import Estudiante, EstudianteCreate, EstudiantePublic
from .horario import Horario, HorarioCreate, HorarioPublic, DiaSemana
from .asignatura import (
    Asignatura, AsignaturaCreate, AsignaturaPublic
)
from .sesion_de_clase import (
    SesionDeClase, SesionDeClaseCreate, SesionDeClaseUpdate,
    EstadoSesion
)
from .registro_asistencia import (
    RegistroAsistencia, RegistroAsistenciaCreate, RegistroAsistenciaUpdate,
    EstadoAsistencia
)
from .inscripcion import Inscripcion, InscripcionCreate
from .clase_programada import ClaseProgramada, ClaseProgramadaCreate

__all__ = [
    "Usuario", "UsuarioCreate", "UsuarioPublic", "UsuarioUpdate",
    "Estudiante", "EstudianteCreate", "EstudiantePublic",
    "Horario", "HorarioCreate", "HorarioPublic", "DiaSemana",
    "Asignatura", "AsignaturaCreate", "AsignaturaPublic",
    "SesionDeClase", "SesionDeClaseCreate", "SesionDeClaseUpdate",
    "EstadoSesion",
    "RegistroAsistencia", "RegistroAsistenciaCreate", "RegistroAsistenciaUpdate",
    "EstadoAsistencia",
    "Inscripcion", "InscripcionCreate",
    "ClaseProgramada", "ClaseProgramadaCreate",
]
