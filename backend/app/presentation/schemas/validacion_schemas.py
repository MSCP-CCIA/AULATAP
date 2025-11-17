"""
Schemas para el flujo de validación de asistencia.
"""
from pydantic import BaseModel, Field

# Schema para la petición de registrar asistencia
class RegistrarAsistenciaRequest(BaseModel):
    codigo_rfid: str = Field(..., description="Código RFID leído del carnet del estudiante")

