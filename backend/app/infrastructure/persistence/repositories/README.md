# Repositorios de Persistencia (Implementaciones)

Este directorio contiene las implementaciones concretas de los repositorios definidos en la capa de dominio. Cada archivo aquí es responsable de interactuar con la base de datos (usando SQLAlchemy) para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) y consultas más complejas para una entidad de dominio específica.

---

### `usuario_repository_impl.py`

**Propósito:** Este archivo proporciona la implementación concreta para la interfaz `IUsuarioRepository`. Maneja todas las operaciones de base de datos relacionadas con la entidad `Usuario` utilizando SQLAlchemy. Traduce entre los DTOs de dominio `UsuarioCreate`, `UsuarioUpdate` y el modelo SQLAlchemy `UsuarioModel`.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy, que se utiliza para todas las comunicaciones con la base de datos.
*   `async def get_by_id(self, usuario_id: uuid.UUID) -> Optional[Usuario]`: Recupera un único usuario de la tabla `Usuario` por su clave primaria (`id`). Si se encuentra, mapea el objeto del modelo SQLAlchemy a una entidad de dominio `Usuario`. De lo contrario, devuelve `None`.
*   `async def get_by_email(self, email: str) -> Optional[Usuario]`: Busca un usuario por su dirección de correo electrónico (`email`). Ejecuta una sentencia `SELECT` y devuelve el primer resultado, mapeado a una entidad de dominio `Usuario`, o `None` si no se encuentra.
*   `async def create(self, usuario_create: UsuarioCreate) -> Usuario`: Crea un nuevo usuario. Primero, hashea la contraseña del DTO `usuario_create` utilizando `get_password_hash`. Luego, crea una nueva instancia de `UsuarioModel`, la rellena con los datos del usuario (incluyendo la contraseña hasheada y el rol), la añade a la sesión y la guarda en la base de datos. Finalmente, devuelve el usuario recién creado como una entidad de dominio `Usuario`.
*   `async def update(self, usuario_id: uuid.UUID, usuario_update: UsuarioUpdate) -> Optional[Usuario]`: Actualiza la información de un usuario existente. Busca el usuario por `id`. Si se encuentra, itera sobre los campos del DTO `usuario_update` y aplica los cambios al modelo SQLAlchemy. Luego, guarda los cambios y devuelve la entidad de dominio `Usuario` actualizada.
*   `async def list_all(self) -> List[Usuario]`: Recupera todos los usuarios de la tabla `Usuario`, ordenados por su nombre completo (`nombre_completo`). Devuelve una lista de entidades de dominio `Usuario`.

---

### `estudiante_repository_impl.py`

**Propósito:** Implementa la interfaz `IEstudianteRepository`. Gestiona las operaciones de base de datos para la entidad `Estudiante`, interactuando con la tabla `Estudiante` en la base de datos.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy.
*   `async def get_by_id(self, estudiante_id: uuid.UUID) -> Optional[Estudiante]`: Obtiene un estudiante por su clave primaria (`id`).
*   `async def get_by_rfc_uid(self, rfc_uid: str) -> Optional[Estudiante]`: Encuentra un estudiante por su `rfc_uid` único (identificador de tarjeta NFC).
*   `async def get_by_email(self, email: str) -> Optional[Estudiante]`: Encuentra un estudiante por su dirección de correo electrónico (`email`).
*   `async def create(self, estudiante_create: EstudianteCreate) -> Estudiante`: Crea un nuevo registro de estudiante en la tabla `Estudiante` a partir de un DTO `EstudianteCreate`.
*   `async def list_all(self) -> List[Estudiante]`: Devuelve una lista de todos los estudiantes, ordenados por su nombre completo.

---

### `asignatura_repository_impl.py`

**Propósito:** Implementa la interfaz `IAsignaturaRepository`. Este repositorio es responsable de las operaciones de datos relacionadas con la entidad `Asignatura` y también para consultar relaciones con otras entidades como `Inscripcion` y `ClaseProgramada`.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy.
*   `async def get_by_id(self, asignatura_id: uuid.UUID) -> Optional[Asignatura]`: Recupera una asignatura por su clave primaria (`id`).
*   `async def list_by_docente(self, docente_id: uuid.UUID) -> List[Asignatura]`: Lista todas las asignaturas impartidas por un docente específico (`docente_id`), ordenadas por nombre.
*   `async def create(self, asignatura_create: AsignaturaCreate) -> Asignatura`: Crea una nueva asignatura.
*   `async def esta_estudiante_inscrito(self, id_asignatura: uuid.UUID, id_estudiante: uuid.UUID) -> bool`: Verifica si un estudiante está inscrito en una asignatura consultando la tabla de unión `Inscripcion`. Devuelve `True` si existe una entrada, `False` en caso contrario.
*   `async def existe_clase_programada(self, id_asignatura: uuid.UUID, id_horario: uuid.UUID) -> bool`: Verifica si una asignatura está programada en un horario específico consultando la tabla de unión `ClaseProgramada`. Devuelve `True` si existe una entrada, `False` en caso contrario.

---

### `horario_repository_impl.py`

**Propósito:** Implementa la interfaz `IHorarioRepository`, gestionando las operaciones de base de datos para la entidad `Horario`.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy.
*   `async def get_by_id(self, horario_id: uuid.UUID) -> Optional[Horario]`: Obtiene un horario por su clave primaria (`id`).
*   `async def create(self, horario_create: HorarioCreate) -> Horario`: Crea un nuevo registro de horario.
*   `async def list_all(self) -> List[Horario]`: Devuelve todos los horarios, ordenados por día de la semana y hora de inicio.

---

### `sesion_de_clase_repository_impl.py`

**Propósito:** Implementa la interfaz `ISesionDeClaseRepository` para gestionar las entidades `SesionDeClase`.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy.
*   `async def get_by_id(self, sesion_id: uuid.UUID) -> Optional[SesionDeClase]`: Recupera una sesión de clase por su clave primaria (`id`).
*   `async def find_activa(self, id_clase: uuid.UUID, id_horario: uuid.UUID) -> Optional[SesionDeClase]`: Encuentra una sesión de clase activa (`EnProgreso`) para una asignatura y horario específicos.
*   `async def create(self, sesion_create: SesionDeClaseCreate) -> SesionDeClase`: Crea una nueva sesión de clase, estableciendo su estado inicial a `EnProgreso` y registrando la hora de inicio.
*   `async def update(self, sesion_id: uuid.UUID, sesion_update: SesionDeClaseUpdate) -> Optional[SesionDeClase]`: Actualiza una sesión de clase, típicamente utilizada para cambiar su estado (por ejemplo, a `Cerrada`) y registrar la hora de finalización.

---

### `registro_asistencia_repository_impl.py`

**Propósito:** Implementa la interfaz `IRegistroAsistenciaRepository` para gestionar las entidades `RegistroAsistencia`.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy.
*   `async def get_by_id(self, registro_id: uuid.UUID) -> Optional[RegistroAsistencia]`: Obtiene un registro de asistencia por su clave primaria (`id`).
*   `async def get_by_sesion_and_estudiante(self, sesion_id: uuid.UUID, estudiante_id: uuid.UUID) -> Optional[RegistroAsistencia]`: Recupera un registro de asistencia específico para un estudiante en una sesión.
*   `async def create(self, registro_create: RegistroAsistenciaCreate) -> RegistroAsistencia`: Crea un nuevo registro de asistencia basado en los datos del DTO `registro_create`, incluyendo la hora de llegada del estudiante y el estado de asistencia (`Presente`, `Tarde`, etc.).
*   `async def update(self, registro_id: uuid.UUID, registro_update: RegistroAsistenciaUpdate) -> Optional[RegistroAsistencia]`: Actualiza un registro de asistencia, por ejemplo, para añadir una hora de salida (`hora_salida`).
*   `async def list_by_sesion(self, sesion_id: uuid.UUID) -> List[RegistroAsistencia]`: Lista todos los registros de asistencia para una sesión de clase determinada.

---

### `inscripcion_repository_impl.py`

**Propósito:** Un nuevo repositorio creado específicamente para manejar la relación `Inscripcion` (Matrícula) entre estudiantes y asignaturas. Implementa la interfaz `IInscripcionRepository`.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy.
*   `async def create(self, inscripcion_create: InscripcionCreate) -> Inscripcion`: Crea un nuevo registro de matrícula en la tabla de unión `Inscripcion`, vinculando un estudiante a una asignatura.
*   `async def get_by_asignatura_and_estudiante(self, id_asignatura: uuid.UUID, id_estudiante: uuid.UUID) -> Optional[Inscripcion]`: Verifica si ya existe un registro de matrícula para un estudiante y una asignatura específicos.

---

### `clase_programada_repository_impl.py`

**Propósito:** Un nuevo repositorio creado para gestionar la relación `ClaseProgramada` (Clase Programada) entre asignaturas y horarios. Implementa la interfaz `IClaseProgramadaRepository`.

**Métodos:**
*   `__init__(self, session: AsyncSession)`: Inicializa el repositorio con una sesión asíncrona de SQLAlchemy.
*   `async def create(self, clase_programada_create: ClaseProgramadaCreate) -> ClaseProgramada`: Crea un nuevo registro en la tabla de unión `ClaseProgramada`, vinculando una asignatura a un horario.
*   `async def get_by_asignatura_and_horario(self, id_asignatura: uuid.UUID, id_horario: uuid.UUID) -> Optional[ClaseProgramada]`: Verifica si una clase ya está programada para una asignatura y un horario específicos.
