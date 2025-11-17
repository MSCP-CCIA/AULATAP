from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user # Importar get_current_active_user
from app.application.use_cases.ListarHorariosUseCase import ListarHorariosUseCase
from app.infrastructure.persistence.repositories.horario_repository_impl import HorarioRepositoryImpl
from app.presentation.schemas.horario_schemas import HorarioPublic

router = APIRouter()


def get_listar_horarios_use_case(db: AsyncSession = Depends(get_db)) -> ListarHorariosUseCase:
    horario_repo = HorarioRepositoryImpl(db)
    return ListarHorariosUseCase(horario_repo)


@router.get(
    "/",
    response_model=List[HorarioPublic],
    status_code=status.HTTP_200_OK,
    summary="Lista todas las franjas horarias.",
    dependencies=[Depends(get_current_active_user)] # Añadir la dependencia de autenticación
)
async def listar_horarios(
    use_case: ListarHorariosUseCase = Depends(get_listar_horarios_use_case)
) -> List[HorarioPublic]:
    """
    Devuelve una lista de todas las franjas horarias disponibles en el sistema.
    Requiere autenticación.
    """
    horarios = await use_case.execute()
    return [HorarioPublic.model_validate(h) for h in horarios]
