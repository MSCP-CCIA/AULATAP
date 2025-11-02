"""
Logging Module
Configuración centralizada del sistema de logging.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
import json
from datetime import datetime

from app.core.config import settings


# ==================== CUSTOM FORMATTER ====================

class JSONFormatter(logging.Formatter):
    """
    Formatter que genera logs en formato JSON estructurado.
    Útil para sistemas de log aggregation (ELK, CloudWatch, etc.)
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Agregar contexto extra si existe
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        # Agregar excepción si existe
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """
    Formatter con colores ANSI para consola (desarrollo).
    """

    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'

    def format(self, record: logging.LogRecord) -> str:
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}"
                f"{record.levelname}{self.RESET}"
            )
        return super().format(record)


# ==================== LOGGER CONFIGURATION ====================

def setup_logging() -> logging.Logger:
    """
    Configura el sistema de logging global.

    Returns:
        Logger raíz configurado
    """
    # Crear logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    # Limpiar handlers existentes (evitar duplicados)
    root_logger.handlers.clear()

    # ==================== CONSOLE HANDLER ====================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)

    if settings.is_development:
        # Formato con colores para desarrollo
        console_formatter = ColoredFormatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        # Formato JSON para producción
        console_formatter = JSONFormatter()

    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # ==================== FILE HANDLER (Opcional) ====================
    if settings.LOG_FILE:
        # Crear directorio de logs si no existe
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Handler con rotación de archivos
        file_handler = RotatingFileHandler(
            filename=settings.LOG_FILE,
            maxBytes=settings.LOG_MAX_BYTES,  # Default: 10MB
            backupCount=settings.LOG_BACKUP_COUNT,  # Default: 5 archivos
            encoding="utf-8"
        )
        file_handler.setLevel(settings.LOG_LEVEL)

        # Siempre JSON en archivos (para parsing)
        file_formatter = JSONFormatter()
        file_handler.setFormatter(file_formatter)

        root_logger.addHandler(file_handler)

    # ==================== SILENCE NOISY LOGGERS ====================
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return root_logger


# ==================== APPLICATION LOGGER ====================

# Configurar logging al importar el módulo
setup_logging()

# Logger específico de la aplicación
logger = logging.getLogger("aulatap")


# ==================== CONTEXT LOGGER ====================

class ContextLogger:
    """
    Logger con contexto adicional (útil para requests HTTP).

    Uso:
        context_logger = ContextLogger(logger, request_id="123", user_id="456")
        context_logger.info("User performed action")
        # Log incluirá request_id y user_id automáticamente
    """

    def __init__(
            self,
            base_logger: logging.Logger,
            **context
    ):
        self.base_logger = base_logger
        self.context = context

    def _log(self, level: int, message: str, **kwargs):
        """Log con contexto adicional."""
        extra = kwargs.get("extra", {})
        extra.update(self.context)
        kwargs["extra"] = extra
        self.base_logger.log(level, message, **kwargs)

    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        self._log(logging.CRITICAL, message, **kwargs)


# ==================== HELPER FUNCTIONS ====================

def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con un nombre específico.

    Args:
        name: Nombre del logger (normalmente __name__ del módulo)

    Returns:
        Logger configurado

    Uso:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.info("Module initialized")
    """
    return logging.getLogger(name)


def log_function_call(func):
    """
    Decorator para loggear llamadas a funciones (útil para debugging).

    Uso:
        @log_function_call
        async def my_function(arg1, arg2):
            # código
    """
    import functools
    import inspect

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        func_logger = get_logger(func.__module__)
        func_logger.debug(
            f"Calling {func.__name__}",
            extra={
                "function": func.__name__,
                "args": str(args)[:100],  # Limitar tamaño
                "kwargs": str(kwargs)[:100]
            }
        )

        try:
            result = await func(*args, **kwargs)
            func_logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            func_logger.error(
                f"{func.__name__} raised {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        func_logger = get_logger(func.__module__)
        func_logger.debug(
            f"Calling {func.__name__}",
            extra={
                "function": func.__name__,
                "args": str(args)[:100],
                "kwargs": str(kwargs)[:100]
            }
        )

        try:
            result = func(*args, **kwargs)
            func_logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            func_logger.error(
                f"{func.__name__} raised {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            raise

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


# ==================== LOG LEVEL HELPERS ====================

def set_log_level(level: str) -> None:
    """
    Cambia el nivel de log dinámicamente.

    Args:
        level: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    logging.getLogger().setLevel(numeric_level)
    logger.info(f"Log level changed to {level}")


def get_current_log_level() -> str:
    """
    Obtiene el nivel de log actual.

    Returns:
        Nombre del nivel de log (DEBUG, INFO, etc.)
    """
    return logging.getLevelName(logging.getLogger().level)