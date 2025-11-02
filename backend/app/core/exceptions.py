"""
Exceptions Module
Define excepciones personalizadas del dominio y handlers para FastAPI.
"""

from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import traceback
from datetime import datetime

from app.core.logger import logger


# ==================== BASE EXCEPTION ====================

class AulaTapException(Exception):
    """
    Excepción base para todas las excepciones personalizadas de AulaTap.
    """

    def __init__(
            self,
            message: str,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


# ==================== AUTHENTICATION & AUTHORIZATION EXCEPTIONS ====================

class UnauthorizedException(AulaTapException):
    """
    Excepción para errores de autenticación (401).
    Lanzada cuando las credenciales son inválidas o el token es inválido/expirado.
    """

    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ForbiddenException(AulaTapException):
    """
    Excepción para errores de autorización (403).
    Lanzada cuando el usuario no tiene permisos suficientes.
    """

    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_403_FORBIDDEN
        )


# ==================== RESOURCE EXCEPTIONS ====================

class NotFoundException(AulaTapException):
    """
    Excepción para recursos no encontrados (404).
    """

    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "identifier": str(identifier)}
        )


class AlreadyExistsException(AulaTapException):
    """
    Excepción para recursos que ya existen (409).
    """

    def __init__(self, resource: str, field: str, value: Any):
        message = f"{resource} with {field}='{value}' already exists"
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details={"resource": resource, "field": field, "value": str(value)}
        )


# ==================== VALIDATION EXCEPTIONS ====================

class ValidationException(AulaTapException):
    """
    Excepción para errores de validación de negocio (400).
    """

    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            message=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"field": field} if field else {}
        )


class InvalidNFCUIDException(ValidationException):
    """
    Excepción específica para UID de NFC inválido.
    """

    def __init__(self, uid: str):
        super().__init__(
            detail=f"Invalid NFC UID format: '{uid}'",
            field="nfc_uid"
        )


class InvalidSessionStateException(ValidationException):
    """
    Excepción cuando se intenta operar sobre una sesión en estado inválido.
    """

    def __init__(self, session_id: str, current_state: str, expected_state: str):
        super().__init__(
            detail=f"Session is in '{current_state}' state, expected '{expected_state}'",
            field="session_id"
        )
        self.details.update({
            "session_id": session_id,
            "current_state": current_state,
            "expected_state": expected_state
        })


# ==================== BUSINESS LOGIC EXCEPTIONS ====================

class DuplicateAttendanceException(AulaTapException):
    """
    Excepción cuando se intenta registrar asistencia duplicada.
    Nota: En práctica se maneja con upsert idempotente, pero útil para logs.
    """

    def __init__(self, session_id: str, student_id: str):
        super().__init__(
            message="Attendance already recorded for this student in this session",
            status_code=status.HTTP_409_CONFLICT,
            details={
                "session_id": session_id,
                "student_id": student_id
            }
        )


class SessionNotActiveException(ValidationException):
    """
    Excepción cuando se intenta registrar asistencia en sesión no activa.
    """

    def __init__(self, session_id: str, status: str):
        super().__init__(
            detail=f"Cannot record attendance: session status is '{status}' (must be 'active')",
            field="session_id"
        )
        self.details.update({
            "session_id": session_id,
            "session_status": status
        })


class StudentNotEnrolledException(ValidationException):
    """
    Excepción cuando estudiante no está inscrito en la clase.
    """

    def __init__(self, student_id: str, class_id: str):
        super().__init__(
            detail="Student is not enrolled in this class",
            field="student_id"
        )
        self.details.update({
            "student_id": student_id,
            "class_id": class_id
        })


# ==================== EXTERNAL SERVICE EXCEPTIONS ====================

class ExternalServiceException(AulaTapException):
    """
    Excepción para errores en servicios externos (SAP, email, etc.)
    """

    def __init__(self, service_name: str, detail: str):
        super().__init__(
            message=f"External service error ({service_name}): {detail}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"service": service_name}
        )


class DatabaseConnectionException(AulaTapException):
    """
    Excepción para errores de conexión a base de datos.
    """

    def __init__(self, detail: str = "Database connection failed"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


# ==================== RATE LIMITING EXCEPTION ====================

class RateLimitException(AulaTapException):
    """
    Excepción para rate limiting (429).
    """

    def __init__(self, detail: str = "Too many requests", retry_after: int = 60):
        super().__init__(
            message=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after_seconds": retry_after}
        )


# ==================== ERROR RESPONSE MODELS ====================

def create_error_response(
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Crea una respuesta de error estandarizada.

    Args:
        status_code: Código HTTP
        message: Mensaje de error
        details: Detalles adicionales (opcional)
        request_id: ID de la request para tracking (opcional)

    Returns:
        Dict con formato estandarizado de error
    """
    error_response = {
        "error": {
            "code": status_code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }

    if details:
        error_response["error"]["details"] = details

    if request_id:
        error_response["error"]["request_id"] = request_id

    return error_response


# ==================== EXCEPTION HANDLERS ====================

async def aulatap_exception_handler(request: Request, exc: AulaTapException) -> JSONResponse:
    """
    Handler para excepciones personalizadas de AulaTap.
    """
    request_id = request.headers.get("X-Request-ID")

    logger.warning(
        f"AulaTap Exception: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "details": exc.details,
            "request_id": request_id,
            "path": request.url.path
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details,
            request_id=request_id
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handler para errores de validación de Pydantic (422).
    """
    request_id = request.headers.get("X-Request-ID")

    # Formatear errores de validación
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(
        "Validation error",
        extra={
            "errors": errors,
            "request_id": request_id,
            "path": request.url.path
        }
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            details={"validation_errors": errors},
            request_id=request_id
        )
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler para excepciones no capturadas (500).
    """
    request_id = request.headers.get("X-Request-ID")

    # Log completo del error con traceback
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )

    # En desarrollo: retornar detalles del error
    # En producción: mensaje genérico
    from app.core.config import settings

    if settings.DEBUG:
        error_detail = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback": traceback.format_exc()
        }
    else:
        error_detail = None

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            details=error_detail,
            request_id=request_id
        )
    )


# ==================== REGISTER HANDLERS FUNCTION ====================

def register_exception_handlers(app) -> None:
    """
    Registra todos los exception handlers en la aplicación FastAPI.

    Args:
        app: Instancia de FastAPI

    Uso:
        from fastapi import FastAPI
        from app.core.exceptions import register_exception_handlers

        app = FastAPI()
        register_exception_handlers(app)
    """
    # Excepciones personalizadas
    app.add_exception_handler(AulaTapException, aulatap_exception_handler)

    # Excepciones de validación
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)

    # Excepciones genéricas
    app.add_exception_handler(Exception, generic_exception_handler)

    logger.info("Exception handlers registered")