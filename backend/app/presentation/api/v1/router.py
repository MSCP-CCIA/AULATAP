from fastapi import APIRouter
from app.presentation.api.v1.endpoints import login, asistencia, horarios, asignaturas, sesiones, validacion

api_v1_router = APIRouter()
api_v1_router.include_router(login.router, tags=["login"])
api_v1_router.include_router(asistencia.router, prefix="/asistencia", tags=["asistencia"])
api_v1_router.include_router(horarios.router, prefix="/horarios", tags=["horarios"])
api_v1_router.include_router(asignaturas.router, prefix="/asignaturas", tags=["asignaturas"])
api_v1_router.include_router(sesiones.router, prefix="/sesiones", tags=["sesiones"])
api_v1_router.include_router(validacion.router, prefix="/sesiones", tags=["validación"])
