from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user # Removed require_role
from app.domain.entities.usuario import Usuario
from app.application.use_cases.GetAsignaturasPorDocenteUseCase import GetAsignaturasPorDocenteUseCase
from app.infrastructure.persistence.repositories.asignatura_repository_impl import AsignaturaRepositoryImpl
from app.presentation.schemas.asignatura_schemas import AsignaturaPublic

router = APIRouter()


def get_asignaturas_por_docente_use_case(db: AsyncSession = Depends(get_db)) -> GetAsignaturasPorDocenteUseCase:
    asignatura_repo = AsignaturaRepositoryImpl(db)
    return GetAsignaturasPorDocenteUseCase(asignatura_repo)


@router.get(
    "/mis-asignaturas",
    response_model=List[AsignaturaPublic],
    status_code=status.HTTP_200_OK,
    summary="Obtiene la lista de asignaturas del docente actualmente autenticado."
    # Removed dependencies=[Depends(require_role(["docente"]))]
)
async def get_mis_asignaturas(
    current_user: Usuario = Depends(get_current_active_user),
    use_case: GetAsignaturasPorDocenteUseCase = Depends(get_asignaturas_por_docente_use_case)
) -> List[AsignaturaPublic]:
    """
    Devuelve una lista de todas las asignaturas impartidas por el docente autenticado.
    Requiere autenticación.
    """
    asignaturas = await use_case.execute(current_user.id)
    return [AsignaturaPublic.model_validate(a) for a in asignaturas]
