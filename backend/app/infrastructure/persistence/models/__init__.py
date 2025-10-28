# en models/__init__.py

# Importa la Base primero
from .base import Base

# Importa todos tus modelos
from .usuario import Usuario
from .estudiante import Estudiante
from .horario import Horario
from .asignatura import Asignatura
from .clase_programada import ClaseProgramada
from .inscripcion import Inscripcion
from .sesion_de_clase import SesionDeClase
from .registro_asistencia import RegistroAsistencia

# Importa los Enums si deseas que sean accesibles
# directamente desde 'models'
from .sesion_de_clase import EstadoSesion
from .registro_asistencia import EstadoAsistencia