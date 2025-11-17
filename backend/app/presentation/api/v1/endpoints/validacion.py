from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.domain.entities.usuario import Usuario
from app.presentation.schemas.validacion_schemas import RegistrarAsistenciaRequest
from app.presentation.schemas.sesion_de_clase_schemas import SesionDeClasePublic
from app.presentation.schemas.registro_asistencia_schemas import RegistroAsistenciaPublic

from app.application.use_cases.AbrirValidacionUseCase import AbrirValidacionUseCase
from app.application.use_cases.RegistrarAsistenciaUseCase import RegistrarAsistenciaUseCase
from app.application.use_cases.CerrarValidacionUseCase import CerrarValidacionUseCase
from app.infrastructure.persistence.repositories import (
    SesionDeClaseRepositoryImpl,
    RegistroAsistenciaRepositoryImpl,
    EstudianteRepositoryImpl,
    InscripcionRepositoryImpl
)
from app.core.exceptions import AulaTapException

router = APIRouter()

def get_abrir_validacion_use_case(db: AsyncSession = Depends(get_db)) -> AbrirValidacionUseCase:
    repo = SesionDeClaseRepositoryImpl(db)
    return AbrirValidacionUseCase(repo)

def get_registrar_asistencia_use_case(db: AsyncSession = Depends(get_db)) -> RegistrarAsistenciaUseCase:
    return RegistrarAsistenciaUseCase(
        sesion_de_clase_repository=SesionDeClaseRepositoryImpl(db),
        registro_asistencia_repository=RegistroAsistenciaRepositoryImpl(db),
        estudiante_repository=EstudianteRepositoryImpl(db),
        inscripcion_repository=InscripcionRepositoryImpl(db)
    )

def get_cerrar_validacion_use_case(db: AsyncSession = Depends(get_db)) -> CerrarValidacionUseCase:
    return CerrarValidacionUseCase(
        sesion_de_clase_repository=SesionDeClaseRepositoryImpl(db),
        inscripcion_repository=InscripcionRepositoryImpl(db),
        registro_asistencia_repository=RegistroAsistenciaRepositoryImpl(db)
    )

@router.post("/{id_sesion}/abrir-validacion", response_model=SesionDeClasePublic, summary="Abrir la validación de asistencia para una sesión")
async def abrir_validacion(
    id_sesion: int,
    use_case: AbrirValidacionUseCase = Depends(get_abrir_validacion_use_case),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Permite a un docente abrir el proceso de validación de asistencia para una sesión de clase que está 'EnProgreso'.
    """
    try:
        sesion = await use_case.execute(id_sesion, current_user.id)
        return sesion
    except AulaTapException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/{id_sesion}/registrar-asistencia", response_model=RegistroAsistenciaPublic, summary="Registrar la asistencia de un estudiante")
async def registrar_asistencia(
    id_sesion: int,
    request: RegistrarAsistenciaRequest,
    use_case: RegistrarAsistenciaUseCase = Depends(get_registrar_asistencia_use_case)
):
    """
    Registra el 'tap' de un carnet de estudiante para una sesión con validación abierta.
    """
    try:
        registro = await use_case.execute(id_sesion, request.codigo_rfid)
        return registro
    except AulaTapException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/{id_sesion}/cerrar-validacion", response_model=SesionDeClasePublic, summary="Cerrar la validación de asistencia")
async def cerrar_validacion(
    id_sesion: int,
    use_case: CerrarValidacionUseCase = Depends(get_cerrar_validacion_use_case),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cierra el proceso de validación, marca a los estudiantes no registrados como ausentes y cambia el estado de la sesión.
    """
    try:
        sesion = await use_case.execute(id_sesion, current_user.id)
        return sesion
    except AulaTapException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
