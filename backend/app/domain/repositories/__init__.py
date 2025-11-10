"""
Paquete de Repositorios de Dominio (Interfaces)

Exporta las interfaces (contratos abstractos) que la capa de aplicación
utilizará para interactuar con la capa de persistencia.
"""

from .usuario_repository import IUsuarioRepository
from .estudiante_repository import IEstudianteRepository
from .horario_repository import IHorarioRepository
from .asignatura_repository import IAsignaturaRepository
from .sesion_de_clase_repository import ISesionDeClaseRepository
from .registro_asistencia_repository import IRegistroAsistenciaRepository
from .inscripcion_repository import IInscripcionRepository
from .clase_programada_repository import IClaseProgramadaRepository

__all__ = [
    "IUsuarioRepository",
    "IEstudianteRepository",
    "IHorarioRepository",
    "IAsignaturaRepository",
    "ISesionDeClaseRepository",
    "IRegistroAsistenciaRepository",
    "IInscripcionRepository",
    "IClaseProgramadaRepository",
]
