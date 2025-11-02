"""
Configuration Module
Gestiona todas las variables de configuración del sistema usando Pydantic Settings.
"""

import os
from typing import List, Optional, ClassVar
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración global de la aplicación.
    Lee variables de entorno y las valida automáticamente.
    """

    # --- Lógica de Ruta para .env ---
    current_file_dir: ClassVar[str] = os.path.dirname(os.path.abspath(__file__))
    core_dir: ClassVar[str] = os.path.dirname(current_file_dir)
    app_dir: ClassVar[str] = os.path.dirname(core_dir)
    ENV_FILE_PATH: ClassVar[str] = os.path.join(app_dir, ".env")

    # ==================== APP SETTINGS ====================
    APP_NAME: str = Field(default="AulaTap API", description="Nombre de la aplicación")
    VERSION: str = Field(default="1.0.0", description="Versión de la API")
    DEBUG: bool = Field(default=False, description="Modo debug (solo desarrollo)")
    ENVIRONMENT: str = Field(default="development", description="Entorno: development|staging|production")

    # ==================== SERVER SETTINGS ====================
    HOST: str = Field(default="0.0.0.0", description="Host del servidor")
    PORT: int = Field(default=8000, description="Puerto del servidor")
    WORKERS: int = Field(default=4, description="Número de workers (producción)")

    # ==================== DATABASE SETTINGS ====================
    DATABASE_URL: str = Field(
        ...,  # Required
        description="URL de conexión a PostgreSQL",
        examples=["postgresql+psycopg://user:pass@localhost:5432/aulatap_db"]  # Actualizado
    )
    DATABASE_POOL_SIZE: int = Field(default=10, description="Tamaño del pool de conexiones")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Conexiones adicionales permitidas")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, description="Timeout del pool en segundos")
    DATABASE_ECHO: bool = Field(default=False, description="Mostrar queries SQL en logs")

    # --- ¡CAMBIO 1: Validador actualizado a 'psycopg'! ---
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Valida que la URL de DB use un driver asíncrono compatible (psycopg)."""
        if not v.startswith("postgresql+psycopg://"):
            raise ValueError("DATABASE_URL debe usar el driver psycopg (postgresql+psycopg://...)")
        return v

    # ==================== SECURITY SETTINGS ====================
    SECRET_KEY: str = Field(
        ...,  # Required
        min_length=32,
        description="Clave secreta para firma de JWT (debe ser compleja)"
    )
    ALGORITHM: str = Field(default="HS256", description="Algoritmo de firma JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, description="Expiración del access token en minutos")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Expiración del refresh token en días")

    PASSWORD_MIN_LENGTH: int = Field(default=8, description="Longitud mínima de contraseñas")
    PASSWORD_REQUIRE_UPPERCASE: bool = Field(default=True)
    PASSWORD_REQUIRE_LOWERCASE: bool = Field(default=True)
    PASSWORD_REQUIRE_DIGIT: bool = Field(default=True)
    PASSWORD_REQUIRE_SPECIAL: bool = Field(default=True)

    # ==================== CORS SETTINGS ====================
    ALLOWED_ORIGINS_STR: str = Field(
        default="*",
        alias="ALLOWED_ORIGINS",
        description="Orígenes permitidos para CORS (separados por coma)"
    )
    ALLOW_CREDENTIALS: bool = Field(default=True, description="Permitir credenciales en CORS")
    ALLOWED_METHODS: List[str] = Field(default=["GET", "POST", "PATCH", "DELETE", "OPTIONS"])
    ALLOWED_HEADERS: List[str] = Field(default=["*"])

    # ==================== LOGGING SETTINGS ====================
    LOG_LEVEL: str = Field(default="INFO", description="Nivel de logging: DEBUG|INFO|WARNING|ERROR|CRITICAL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Formato de logs"
    )
    LOG_FILE: Optional[str] = Field(default=None, description="Archivo de logs (None = solo consola)")
    LOG_MAX_BYTES: int = Field(default=10485760, description="Tamaño máximo del log file (10MB)")
    LOG_BACKUP_COUNT: int = Field(default=5, description="Número de archivos de backup")

    # ... (El resto de tus settings que estaban bien) ...
    REDIS_URL: Optional[str] = Field(default=None)
    REDIS_CACHE_TTL: int = Field(default=300)
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    RATE_LIMIT_LOGIN_ATTEMPTS: int = Field(default=5)
    NFC_UID_MIN_LENGTH: int = Field(default=8)
    NFC_UID_MAX_LENGTH: int = Field(default=50)
    NFC_UID_PATTERN: str = Field(default=r"^[0-9A-F:]{8,50}$")
    SESSION_LATE_TOLERANCE_MINUTES: int = Field(default=15)
    SESSION_MAX_DURATION_HOURS: int = Field(default=6)
    SYNC_BATCH_MAX_SIZE: int = Field(default=100)
    SYNC_RETRY_MAX_ATTEMPTS: int = Field(default=3)
    SYNC_RETRY_BACKOFF_FACTOR: int = Field(default=2)
    SMTP_HOST: Optional[str] = Field(default=None)
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: Optional[str] = Field(default=None)
    SMTP_PASSWORD: Optional[str] = Field(default=None)
    SMTP_FROM_EMAIL: str = Field(default="noreply@aulatap.edu.co")
    SAP_API_URL: Optional[str] = Field(default=None)
    SAP_CLIENT_ID: Optional[str] = Field(default=None)
    SAP_CLIENT_SECRET: Optional[str] = Field(default=None)
    SENTRY_DSN: Optional[str] = Field(default=None)
    PROMETHEUS_ENABLED: bool = Field(default=False)

    # ==================== MODEL CONFIG ====================

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # ==================== COMPUTED PROPERTIES ====================

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Parsea ALLOWED_ORIGINS_STR en una lista."""
        if not self.ALLOWED_ORIGINS_STR:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_STR.split(",")]

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    # --- ¡CAMBIO 2: Propiedad sync actualizada a 'psycopg'! ---
    @property
    def database_url_sync(self) -> str:
        """Retorna URL síncrona para Alembic (migraciones)."""
        return self.DATABASE_URL.replace("+psycopg", "")


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna instancia singleton de Settings (cacheada).
    """
    return Settings()


# Exportar singleton
settings = get_settings()

