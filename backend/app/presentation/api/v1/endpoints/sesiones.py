from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user # Removed require_role
from app.core.exceptions import ForbiddenException, NotFoundException, ValidationException
from app.domain.entities.usuario import Usuario
from app.domain.entities.sesion_de_clase import SesionDeClase
from app.application.use_cases.AbrirSesionUseCase import AbrirSesionUseCase
from app.application.use_cases.CerrarSesionUseCase import CerrarSesionUseCase
from app.application.use_cases.GetSesionesActivasPorDocenteUseCase import GetSesionesActivasPorDocenteUseCase # New import
from app.infrastructure.persistence.repositories.sesion_de_clase_repository_impl import SesionDeClaseRepositoryImpl
from app.infrastructure.persistence.repositories.asignatura_repository_impl import AsignaturaRepositoryImpl
from app.infrastructure.persistence.repositories.clase_programada_repository_impl import ClaseProgramadaRepositoryImpl
from app.presentation.schemas.sesion_de_clase_schemas import AbrirSesionRequest, SesionDeClasePublic
from app.presentation.schemas.clase_programada_schemas import ClaseProgramadaPublic
from app.presentation.schemas.asignatura_schemas import AsignaturaPublic # New import
from app.presentation.schemas.horario_schemas import HorarioPublic # New import
from app.presentation.schemas.usuario_schemas import UsuarioPublic # New import

router = APIRouter()


def get_abrir_sesion_use_case(db: AsyncSession = Depends(get_db)) -> AbrirSesionUseCase:
    sesion_repo = SesionDeClaseRepositoryImpl(db)
    asignatura_repo = AsignaturaRepositoryImpl(db)
    clase_programada_repo = ClaseProgramadaRepositoryImpl(db)
    return AbrirSesionUseCase(sesion_repo, asignatura_repo, clase_programada_repo)


def get_cerrar_sesion_use_case(db: AsyncSession = Depends(get_db)) -> CerrarSesionUseCase:
    sesion_repo = SesionDeClaseRepositoryImpl(db)
    asignatura_repo = AsignaturaRepositoryImpl(db)
    clase_programada_repo = ClaseProgramadaRepositoryImpl(db)
    return CerrarSesionUseCase(sesion_repo, asignatura_repo, clase_programada_repo)


def get_sesiones_activas_por_docente_use_case(db: AsyncSession = Depends(get_db)) -> GetSesionesActivasPorDocenteUseCase:
    sesion_repo = SesionDeClaseRepositoryImpl(db)
    asignatura_repo = AsignaturaRepositoryImpl(db)
    clase_programada_repo = ClaseProgramadaRepositoryImpl(db)
    return GetSesionesActivasPorDocenteUseCase(sesion_repo, asignatura_repo, clase_programada_repo)


@router.post(
    "/abrir",
    response_model=SesionDeClasePublic,
    status_code=status.HTTP_201_CREATED,
    summary="Un docente inicia una sesión de clase."
    # Removed dependencies=[Depends(require_role(["docente"]))]
)
async def abrir_sesion(
    request: AbrirSesionRequest,
    current_user: Usuario = Depends(get_current_active_user),
    use_case: AbrirSesionUseCase = Depends(get_abrir_sesion_use_case),
    db: AsyncSession = Depends(get_db) # Add db dependency
) -> SesionDeClasePublic: # Changed return type hint to SesionDeClasePublic
    """
    Permite a un docente iniciar una nueva sesión de clase.
    Verifica que el docente sea dueño de la asignatura y que la clase esté programada.
    """
    try:
        sesion, clase_programada = await use_case.execute( # Unpack the tuple
            docente_id=current_user.id,
            id_asignatura=request.id_asignatura,
            id_horario=request.id_horario,
            tema=request.tema
        )
        await db.commit() # Commit the changes

        # Manually construct AsignaturaPublic with current_user as docente
        asignatura_public_with_docente = AsignaturaPublic.model_validate(clase_programada.asignatura)
        asignatura_public_with_docente.docente = UsuarioPublic.model_validate(current_user)

        # Manually construct ClaseProgramadaPublic with the modified AsignaturaPublic
        clase_programada_public = ClaseProgramadaPublic(
            asignatura=asignatura_public_with_docente,
            horario=HorarioPublic.model_validate(clase_programada.horario) # Assuming HorarioPublic can validate directly
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
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post(
    "/{id_sesion}/cerrar",
    response_model=SesionDeClasePublic,
    status_code=status.HTTP_200_OK,
    summary="Un docente cierra una sesión de clase."
)
async def cerrar_sesion(
    id_sesion: int,
    current_user: Usuario = Depends(get_current_active_user),
    use_case: CerrarSesionUseCase = Depends(get_cerrar_sesion_use_case),
    db: AsyncSession = Depends(get_db) # Add db dependency
) -> SesionDeClasePublic: # Changed return type hint to SesionDeClasePublic
    """
    Permite a un docente cerrar una sesión de clase activa.
    Verifica que la sesión exista, esté en progreso y que el docente sea dueño de la asignatura asociada.
    """
    try:
        sesion_cerrada, clase_programada = await use_case.execute(sesion_id=id_sesion, docente_id=current_user.id) # Unpack the tuple
        await db.commit() # Commit the changes

        # Manually construct AsignaturaPublic with current_user as docente
        asignatura_public_with_docente = AsignaturaPublic.model_validate(clase_programada.asignatura)
        asignatura_public_with_docente.docente = UsuarioPublic.model_validate(current_user)

        # Manually construct ClaseProgramadaPublic with the modified AsignaturaPublic
        clase_programada_public = ClaseProgramadaPublic(
            asignatura=asignatura_public_with_docente,
            horario=HorarioPublic.model_validate(clase_programada.horario) # Assuming HorarioPublic can validate directly
        )

        return SesionDeClasePublic(
            id=sesion_cerrada.id,
            hora_inicio=sesion_cerrada.hora_inicio,
            hora_fin=sesion_cerrada.hora_fin,
            estado=sesion_cerrada.estado,
            tema=sesion_cerrada.tema,
            clase_programada=clase_programada_public
        )
    except NotFoundException as e:
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        await db.rollback() # Rollback on exception
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/abiertas",
    response_model=List[SesionDeClasePublic],
    status_code=status.HTTP_200_OK,
    summary="Devuelve las sesiones activas del docente."
)
async def get_sesiones_abiertas(
    current_user: Usuario = Depends(get_current_active_user),
    use_case: GetSesionesActivasPorDocenteUseCase = Depends(get_sesiones_activas_por_docente_use_case)
) -> List[SesionDeClasePublic]:
    """
    Devuelve una lista de todas las sesiones de clase que están actualmente activas
    para el docente autenticado.
    """
    try:
        sesiones_con_clase_programada = await use_case.execute(docente_id=current_user.id)
        response_sesiones = []
        for sesion, clase_programada in sesiones_con_clase_programada:
            # Manually construct AsignaturaPublic with current_user as docente
            asignatura_public_with_docente = AsignaturaPublic.model_validate(clase_programada.asignatura)
            asignatura_public_with_docente.docente = UsuarioPublic.model_validate(current_user)

            # Manually construct ClaseProgramadaPublic with the modified AsignaturaPublic
            clase_programada_public = ClaseProgramadaPublic(
                asignatura=asignatura_public_with_docente,
                horario=HorarioPublic.model_validate(clase_programada.horario) # Assuming HorarioPublic can validate directly
            )

            response_sesiones.append(
                SesionDeClasePublic(
                    id=sesion.id,
                    hora_inicio=sesion.hora_inicio,
                    hora_fin=sesion.hora_fin,
                    estado=sesion.estado,
                    tema=sesion.tema,
                    clase_programada=clase_programada_public
                )
            )
        return response_sesiones
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
