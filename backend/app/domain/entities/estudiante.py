"""
Define la entidad de negocio 'Estudiante'.
"""

from pydantic import BaseModel, EmailStr, Field


class EstudianteBase(BaseModel):
    """Modelo base para Estudiante."""
    email: EmailStr = Field(..., description="Email único del estudiante")
    nombre_completo: str = Field(..., max_length=50, description="Nombre del estudiante")
    rfc_uid: str = Field(..., max_length=50, description="RFC o UID de la tarjeta NFC")


class Estudiante(EstudianteBase):
    """Modelo completo de la entidad Estudiante."""
    id: int

    class Config:
        from_attributes = True


class EstudianteCreate(EstudianteBase):
    """Modelo para crear un nuevo Estudiante."""
    pass  # Por ahora, igual que el base


class EstudiantePublic(EstudianteBase):
    """Modelo seguro para retornar al cliente."""
    id: int

    class Config:
        from_attributes = True
