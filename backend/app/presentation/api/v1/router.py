from fastapi import APIRouter
from app.presentation.api.v1.endpoints import login

api_v1_router = APIRouter()
api_v1_router.include_router(login.router, tags=["login"])
