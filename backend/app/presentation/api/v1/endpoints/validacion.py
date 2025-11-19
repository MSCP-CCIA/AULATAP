from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.domain.entities.usuario import Usuario
from app.presentation.schemas.validacion_schemas import RegistrarAsistenciaRequest
from app.presentation.schemas.sesion_de_clase_schemas import SesionDeClasePublic
from app.presentation.schemas.registro_asistencia_schemas import RegistroAsistenciaPublic, EstudianteInfo, AsignaturaInfo
from app.presentation.schemas.clase_programada_schemas import ClaseProgramadaPublic
from app.presentation.schemas.asignatura_schemas import AsignaturaPublic
from app.presentation.schemas.horario_schemas import HorarioPublic
from app.presentation.schemas.usuario_schemas import UsuarioPublic


from app.application.use_cases.AbrirValidacionUseCase import AbrirValidacionUseCase
from app.application.use_cases.RegistrarAsistenciaUseCase import RegistrarAsistenciaUseCase
from app.application.use_cases.RegistrarAsistenciaValidacionUseCase import RegistrarAsistenciaValidacionUseCase
from app.application.use_cases.CerrarValidacionUseCase import CerrarValidacionUseCase
from app.infrastructure.persistence.repositories import (
    SesionDeClaseRepositoryImpl,
    RegistroAsistenciaRepositoryImpl,
    EstudianteRepositoryImpl,
    InscripcionRepositoryImpl,
    AsignaturaRepositoryImpl,
    ClaseProgramadaRepositoryImpl
)
from app.core.exceptions import AulaTapException, NotFoundException, ForbiddenException, ValidationException

router = APIRouter()

def get_abrir_validacion_use_case(db: AsyncSession = Depends(get_db)) -> AbrirValidacionUseCase:
    sesion_repo = SesionDeClaseRepositoryImpl(db)
    asignatura_repo = AsignaturaRepositoryImpl(db)
    clase_programada_repo = ClaseProgramadaRepositoryImpl(db)
    return AbrirValidacionUseCase(sesion_repo, asignatura_repo, clase_programada_repo)

def get_registrar_asistencia_use_case(db: AsyncSession = Depends(get_db)) -> RegistrarAsistenciaUseCase:
    return RegistrarAsistenciaUseCase(
        sesion_de_clase_repository=SesionDeClaseRepositoryImpl(db),
        registro_asistencia_repository=RegistroAsistenciaRepositoryImpl(db),
        estudiante_repository=EstudianteRepositoryImpl(db),
        inscripcion_repository=InscripcionRepositoryImpl(db)
    )

def get_cerrar_validacion_use_case(db: AsyncSession = Depends(get_db)) -> CerrarValidacionUseCase:
    sesion_repo = SesionDeClaseRepositoryImpl(db)
    inscripcion_repo = InscripcionRepositoryImpl(db)
    registro_asistencia_repo = RegistroAsistenciaRepositoryImpl(db)
    asignatura_repo = AsignaturaRepositoryImpl(db)
    clase_programada_repo = ClaseProgramadaRepositoryImpl(db)
    return CerrarValidacionUseCase(sesion_repo, inscripcion_repo, registro_asistencia_repo, asignatura_repo, clase_programada_repo)

def get_registrar_asistencia_validacion_use_case(db: AsyncSession = Depends(get_db)) -> RegistrarAsistenciaValidacionUseCase:
    return RegistrarAsistenciaValidacionUseCase(
        registro_asistencia_repository=RegistroAsistenciaRepositoryImpl(db),
        sesion_de_clase_repository=SesionDeClaseRepositoryImpl(db),
        estudiante_repository=EstudianteRepositoryImpl(db),
        clase_programada_repository=ClaseProgramadaRepositoryImpl(db) # Added
    )

@router.post("/{id_sesion}/abrir-validacion", response_model=SesionDeClasePublic, summary="Abrir la validación de asistencia para una sesión")
async def abrir_validacion(
    id_sesion: int,
    use_case: AbrirValidacionUseCase = Depends(get_abrir_validacion_use_case),
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Permite a un docente abrir el proceso de validación de asistencia para una sesión de clase que está 'EnProgreso'.
    """
    try:
        sesion, clase_programada = await use_case.execute(id_sesion, current_user.id)
        await db.commit()

        asignatura_public_with_docente = AsignaturaPublic.model_validate(clase_programada.asignatura)
        asignatura_public_with_docente.docente = UsuarioPublic.model_validate(current_user)

        clase_programada_public = ClaseProgramadaPublic(
            asignatura=asignatura_public_with_docente,
            horario=HorarioPublic.model_validate(clase_programada.horario)
        )

        return SesionDeClasePublic(
            id=sesion.id,
            hora_inicio=sesion.hora_inicio,
            hora_fin=sesion.hora_fin,
            estado=sesion.estado,
            tema=sesion.tema,
            clase_programada=clase_programada_public
        )
    except NotFoundException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except AulaTapException as e:
        await db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/{id_sesion}/validar-asistencia", response_model=RegistroAsistenciaPublic, summary="Validar la asistencia de un estudiante")
async def registrar_asistencia(
    id_sesion: int,
    request: RegistrarAsistenciaRequest,
    use_case: RegistrarAsistenciaValidacionUseCase = Depends(get_registrar_asistencia_validacion_use_case),
    db: AsyncSession = Depends(get_db)
):
    """
    Registra el 'tap' de un carnet de estudiante para una sesión con validación abierta.
    """
    try:
        registro, estudiante, clase_programada, sesion = await use_case.execute(id_sesion, request.codigo_rfid)
        await db.commit()

        estudiante_info = EstudianteInfo(nombre_completo=f"{estudiante.nombre_completo}")
        asignatura_info = AsignaturaInfo(
            nombre_materia=clase_programada.asignatura.nombre_materia,
            grupo=clase_programada.asignatura.grupo
        )

        return RegistroAsistenciaPublic(
            id=registro.id,
            hora_entrada=registro.hora_entrada,
            estado_asistencia=registro.estado_asistencia,
            estudiante=estudiante_info,
            asignatura=asignatura_info,
            tema_sesion=sesion.tema
        )
    except NotFoundException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except AulaTapException as e:
        await db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/{id_sesion}/cerrar-validacion", response_model=SesionDeClasePublic, summary="Cerrar la validación de asistencia")
async def cerrar_validacion(
    id_sesion: int,
    use_case: CerrarValidacionUseCase = Depends(get_cerrar_validacion_use_case),
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cierra el proceso de validación, marca a los estudiantes no registrados como ausentes y cambia el estado de la sesión.
    """
    try:
        sesion, clase_programada = await use_case.execute(id_sesion, current_user.id)
        await db.commit()

        asignatura_public_with_docente = AsignaturaPublic.model_validate(clase_programada.asignatura)
        asignatura_public_with_docente.docente = UsuarioPublic.model_validate(current_user)

        clase_programada_public = ClaseProgramadaPublic(
            asignatura=asignatura_public_with_docente,
            horario=HorarioPublic.model_validate(clase_programada.horario)
        )

        return SesionDeClasePublic(
            id=sesion.id,
            hora_inicio=sesion.hora_inicio,
            hora_fin=sesion.hora_fin,
            estado=sesion.estado,
            tema=sesion.tema,
            clase_programada=clase_programada_public
        )
    except NotFoundException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except AulaTapException as e:
        await db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/{id_sesion}/cerrar-validacion", response_model=SesionDeClasePublic, summary="Cerrar la validación de asistencia")
async def cerrar_validacion(
    id_sesion: int,
    use_case: CerrarValidacionUseCase = Depends(get_cerrar_validacion_use_case),
    current_user: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cierra el proceso de validación, marca a los estudiantes no registrados como ausentes y cambia el estado de la sesión.
    """
    try:
        sesion, clase_programada = await use_case.execute(id_sesion, current_user.id)
        await db.commit()

        asignatura_public_with_docente = AsignaturaPublic.model_validate(clase_programada.asignatura)
        asignatura_public_with_docente.docente = UsuarioPublic.model_validate(current_user)

        clase_programada_public = ClaseProgramadaPublic(
            asignatura=asignatura_public_with_docente,
            horario=HorarioPublic.model_validate(clase_programada.horario)
        )

        return SesionDeClasePublic(
            id=sesion.id,
            hora_inicio=sesion.hora_inicio,
            hora_fin=sesion.hora_fin,
            estado=sesion.estado,
            tema=sesion.tema,
            clase_programada=clase_programada_public
        )
    except NotFoundException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except AulaTapException as e:
        await db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
