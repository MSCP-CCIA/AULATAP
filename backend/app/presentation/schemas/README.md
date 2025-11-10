# Schemas Overview

This directory contains the Pydantic schemas used for data validation and serialization within the API. These schemas define the structure of request and response bodies, ensuring data consistency and providing clear documentation for API consumers.

---

## `usuario_schemas.py`

Defines schemas related to the `Usuario` (User/Teacher) entity.

### `UsuarioBase`
Base model for common user fields.
- `email`: `EmailStr` (required) - User's email address. Example: "profesor@example.com"
- `nombre_completo`: `str` (required) - User's full name. Min length: 3, Max length: 50. Example: "Juan Pérez"

### `UsuarioCreate`
Schema for creating a new user.
- Inherits from `UsuarioBase`.
- `password`: `str` (required) - User's password. Min length: 8. Example: "una_contraseña_segura"

### `UsuarioUpdate`
Schema for updating an existing user. All fields are optional.
- `email`: `Optional[EmailStr]` - User's email address. Example: "profesor_nuevo@example.com"
- `nombre_completo`: `Optional[str]` - User's full name. Min length: 3, Max length: 50. Example: "Juan Alberto Pérez"
- `password`: `Optional[str]` - User's password. Min length: 8. Example: "otra_contraseña_mas_segura"

### `UsuarioInDB`
Schema representing the user as stored in the database.
- Inherits from `UsuarioBase`.
- `id`: `uuid.UUID` - Unique identifier for the user.
- `password_hash`: `str` - Hashed password of the user.
- `Config`: `from_attributes = True`

### `UsuarioPublic`
Schema for public responses, omitting sensitive information.
- Inherits from `UsuarioBase`.
- `id`: `uuid.UUID` - Unique identifier for the user.
- `Config`: `from_attributes = True`

### `Token`
Schema for authentication tokens.
- `access_token`: `str` - The JWT access token.
- `token_type`: `str` - Type of the token (e.g., "bearer").

### `TokenData`
Schema for data contained within the JWT token.
- `email`: `Optional[str]` - User's email, if present in the token.

---

## `asignatura_schemas.py`

Defines schemas related to the `Asignatura` (Course/Subject) entity.

### `AsignaturaBase`
Base model for common course fields.
- `nombre_materia`: `str` (required) - Name of the subject. Min length: 3, Max length: 50. Example: "Cálculo I"
- `grupo`: `str` (required) - Group identifier for the subject. Max length: 10. Example: "Grupo A"
- `id_docente`: `uuid.UUID` (required) - UUID of the teacher assigned to the subject.

### `AsignaturaCreate`
Schema for creating a new course.
- Inherits from `AsignaturaBase`.

### `AsignaturaUpdate`
Schema for updating an existing course. All fields are optional.
- `nombre_materia`: `Optional[str]` - Name of the subject. Min length: 3, Max length: 50. Example: "Cálculo Avanzado"
- `grupo`: `Optional[str]` - Group identifier. Max length: 10. Example: "Grupo B"
- `id_docente`: `Optional[uuid.UUID]` - UUID of the assigned teacher.

### `AsignaturaPublic`
Schema for public responses of a course.
- Inherits from `AsignaturaBase`.
- `id`: `uuid.UUID` - Unique identifier for the course.
- `docente`: `Optional[UsuarioPublic]` - Nested `UsuarioPublic` schema for the assigned teacher.
- `Config`: `from_attributes = True`

---

## `clase_programada_schemas.py`

Defines schemas related to the `ClaseProgramada` (Scheduled Class) entity, representing an association between a subject and a schedule.

### `ClaseProgramadaBase`
Base model for scheduled class fields.
- `id_asignatura`: `uuid.UUID` (required) - UUID of the associated subject.
- `id_horario`: `uuid.UUID` (required) - UUID of the associated schedule.

### `ClaseProgramadaCreate`
Schema for creating a new scheduled class.
- Inherits from `ClaseProgramadaBase`.

### `ClaseProgramadaPublic`
Schema for public responses of a scheduled class.
- `asignatura`: `AsignaturaPublic` - Nested `AsignaturaPublic` schema.
- `horario`: `HorarioPublic` - Nested `HorarioPublic` schema.
- `Config`: `from_attributes = True`

---

## `estudiante_schemas.py`

Defines schemas related to the `Estudiante` (Student) entity.

### `EstudianteBase`
Base model for common student fields.
- `email`: `EmailStr` (required) - Student's email address. Example: "estudiante@example.com"
- `nombre_completo`: `str` (required) - Student's full name. Min length: 3, Max length: 50. Example: "Ana Gómez"
- `rfc_uid`: `str` (required) - RFC or UID from the NFC card. Max length: 50. Example: "GOMA881122ABC"

### `EstudianteCreate`
Schema for creating a new student.
- Inherits from `EstudianteBase`.

### `EstudianteUpdate`
Schema for updating an existing student. All fields are optional.
- `email`: `Optional[EmailStr]` - Student's email address. Example: "ana.gomez@example.com"
- `nombre_completo`: `Optional[str]` - Student's full name. Min length: 3, Max length: 50. Example: "Ana María Gómez"
- `rfc_uid`: `Optional[str]` - RFC or UID from the NFC card. Max length: 50. Example: "GOMA881122XYZ"

### `EstudiantePublic`
Schema for public responses of a student.
- Inherits from `EstudianteBase`.
- `id`: `uuid.UUID` - Unique identifier for the student.
- `Config`: `from_attributes = True`

---

## `horario_schemas.py`

Defines schemas related to the `Horario` (Schedule) entity.

### `DiaSemana`
Enum for days of the week.
- `LUNES` = "Lunes"
- `MARTES` = "Martes"
- `MIERCOLES` = "Miércoles"
- `JUEVES` = "Jueves"
- `VIERNES` = "Viernes"
- `SABADO` = "Sábado"
- `DOMINGO` = "Domingo"

### `HorarioBase`
Base model for common schedule fields.
- `dia_semana`: `DiaSemana` (required) - Day of the week. Example: "Lunes"
- `hora_inicio`: `datetime.time` (required) - Start time. Example: "08:00:00"
- `hora_fin`: `datetime.time` (required) - End time. Example: "10:00:00"
- **Validation**: `hora_fin` must be after `hora_inicio`.

### `HorarioCreate`
Schema for creating a new schedule.
- Inherits from `HorarioBase`.

### `HorarioUpdate`
Schema for updating an existing schedule. All fields are optional.
- `dia_semana`: `Optional[DiaSemana]` - Day of the week. Example: "Martes"
- `hora_inicio`: `Optional[datetime.time]` - Start time. Example: "09:00:00"
- `hora_fin`: `Optional[datetime.time]` - End time. Example: "11:00:00"

### `HorarioPublic`
Schema for public responses of a schedule.
- Inherits from `HorarioBase`.
- `id`: `uuid.UUID` - Unique identifier for the schedule.
- `Config`: `from_attributes = True`

---

## `inscripcion_schemas.py`

Defines schemas related to the `Inscripcion` (Enrollment) entity, representing an association between a subject and a student.

### `InscripcionBase`
Base model for enrollment fields.
- `id_asignatura`: `uuid.UUID` (required) - UUID of the associated subject.
- `id_estudiante`: `uuid.UUID` (required) - UUID of the associated student.

### `InscripcionCreate`
Schema for creating a new enrollment.
- Inherits from `InscripcionBase`.

### `InscripcionPublic`
Schema for public responses of an enrollment.
- `fecha_inscripcion`: `date` - Date of enrollment.
- `asignatura`: `AsignaturaPublic` - Nested `AsignaturaPublic` schema.
- `estudiante`: `EstudiantePublic` - Nested `EstudiantePublic` schema.
- `Config`: `from_attributes = True`

---

## `registro_asistencia_schemas.py`

Defines schemas related to the `RegistroAsistencia` (Attendance Record) entity.

### `EstadoAsistencia`
Enum for attendance states.
- `PRESENTE` = "Presente"
- `AUSENTE` = "Ausente"
- `TARDE` = "Tarde"

### `AsistenciaTapCreate`
Schema for recording attendance via NFC card tap.
- `rfc_uid`: `str` (required) - RFC or UID read from the NFC card.
- `id_sesion_clase`: `uuid.UUID` (required) - UUID of the current class session.

### `RegistroAsistenciaCreate`
Schema for manual creation of an attendance record.
- `id_sesion_clase`: `uuid.UUID` (required) - UUID of the class session.
- `id_estudiante`: `uuid.UUID` (required) - UUID of the student.
- `estado_asistencia`: `EstadoAsistencia` - Attendance status. Default: "Presente".

### `RegistroAsistenciaUpdate`
Schema for updating an existing attendance record. All fields are optional.
- `estado_asistencia`: `Optional[EstadoAsistencia]` - Attendance status.

### `RegistroAsistenciaPublic`
Schema for public responses of an attendance record.
- `id`: `uuid.UUID` - Unique identifier for the attendance record.
- `hora_entrada`: `Optional[datetime]` - Time of entry.
- `hora_salida`: `Optional[datetime]` - Time of exit.
- `estado_asistencia`: `EstadoAsistencia` - Attendance status.
- `estudiante`: `EstudiantePublic` - Nested `EstudiantePublic` schema.
- `Config`: `from_attributes = True`

---

## `sesion_de_clase_schemas.py`

Defines schemas related to the `SesionDeClase` (Class Session) entity.

### `EstadoSesion`
Enum for class session states.
- `EN_PROGRESO` = "EnProgreso"
- `CERRADA` = "Cerrada"

### `SesionDeClaseBase`
Base model for common class session fields.
- `id_clase_programada`: `uuid.UUID` (required) - UUID of the scheduled class.
- `tema`: `Optional[str]` - Topic of the class session. Max length: 100. Example: "Introducción a las Derivadas"

### `SesionDeClaseCreate`
Schema for creating a new class session (e.g., when opening a session).
- `id_clase_programada`: `uuid.UUID` (required) - UUID of the scheduled class.
- `tema`: `Optional[str]` - Topic of the class session. Max length: 100.

### `SesionDeClaseUpdate`
Schema for updating an existing class session (e.g., when closing a session). All fields are optional.
- `estado`: `Optional[EstadoSesion]` - Session status. Example: "Cerrada"
- `tema`: `Optional[str]` - Topic of the class session. Max length: 100.

### `SesionDeClasePublic`
Schema for public responses of a class session.
- `id`: `uuid.UUID` - Unique identifier for the class session.
- `hora_inicio`: `datetime` - Start time of the session.
- `hora_fin`: `Optional[datetime]` - End time of the session.
- `estado`: `EstadoSesion` - Current status of the session.
- `tema`: `Optional[str]` - Topic of the class session.
- `clase_programada`: `ClaseProgramadaPublic` - Nested `ClaseProgramadaPublic` schema.
- `Config`: `from_attributes = True`
