
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import NotFoundException, ValidationException
from app.application.use_cases.RegistrarAsistenciaUseCase import RegistrarAsistenciaUseCase
from app.infrastructure.persistence.repositories.registro_asistencia_repository_impl import RegistroAsistenciaRepositoryImpl
from app.infrastructure.persistence.repositories.sesion_de_clase_repository_impl import SesionDeClaseRepositoryImpl
from app.infrastructure.persistence.repositories.estudiante_repository_impl import EstudianteRepositoryImpl
from app.infrastructure.persistence.repositories.inscripcion_repository_impl import InscripcionRepositoryImpl
from app.infrastructure.persistence.repositories.asignatura_repository_impl import AsignaturaRepositoryImpl
from app.presentation.schemas.registro_asistencia_schemas import RegistrarAsistenciaRequest, RegistroAsistenciaPublic, EstudianteInfo, AsignaturaInfo

router = APIRouter()


def get_registrar_asistencia_use_case(db: AsyncSession = Depends(get_db)) -> RegistrarAsistenciaUseCase:
    asistencia_repo = RegistroAsistenciaRepositoryImpl(db)
    sesion_repo = SesionDeClaseRepositoryImpl(db)
    estudiante_repo = EstudianteRepositoryImpl(db)
    inscripcion_repo = InscripcionRepositoryImpl(db)
    return RegistrarAsistenciaUseCase(asistencia_repo, sesion_repo, estudiante_repo, inscripcion_repo)


@router.post(
    "/registrar",
    response_model=RegistroAsistenciaPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Registra la asistencia de un estudiante mediante 'tap' NFC."
)
async def registrar_asistencia(
    request: RegistrarAsistenciaRequest,
    use_case: RegistrarAsistenciaUseCase = Depends(get_registrar_asistencia_use_case),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para el 'tap' de la tarjeta NFC.

    El backend determina automáticamente a qué sesión activa debe registrarse el estudiante.
    """
    try:
        registro = await use_case.execute(request.rfc_uid_estudiante)

        # Construir la respuesta pública
        estudiante_repo = EstudianteRepositoryImpl(db)
        asignatura_repo = AsignaturaRepositoryImpl(db)
        sesion_repo = SesionDeClaseRepositoryImpl(db)

        estudiante = await estudiante_repo.get_by_id(registro.id_estudiante)
        sesion = await sesion_repo.get_by_id(registro.id_sesion_clase)
        asignatura = await asignatura_repo.get_by_id(sesion.id_clase)

        if not estudiante or not sesion or not asignatura:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se pudieron cargar los datos para la respuesta.")

        return RegistroAsistenciaPublic(
            id=registro.id,
            hora_entrada=registro.hora_entrada,
            estado_asistencia=registro.estado_asistencia,
            estudiante=EstudianteInfo.model_validate(estudiante),
            asignatura=AsignaturaInfo.model_validate(asignatura),
            tema_sesion=sesion.tema
        )

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
