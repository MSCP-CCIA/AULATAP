# Casos de Uso de la Aplicación

Este directorio contiene la lógica de negocio central de la aplicación, encapsulada en clases de "Casos de Uso" (Use Cases). Cada archivo representa una única acción o flujo de trabajo que el sistema puede realizar. Estos casos de uso orquestan los repositorios y las entidades del dominio para aplicar las reglas de negocio.

---

### `AbrirSesionUseCase.py`

**Propósito:** Este caso de uso encapsula la lógica de negocio para que un docente abra una nueva sesión de clase. Asegura que se cumplan todas las precondiciones antes de que pueda comenzar una sesión.

**Dependencias:**
*   `ISesionDeClaseRepository`: Para interactuar con los datos de las sesiones de clase.
*   `IAsignaturaRepository`: Para interactuar con los datos de las asignaturas.

**Método `execute`:**
*   **Parámetros:** `id_asignatura`, `id_horario`, `id_docente`, `tema` (opcional).
*   **Lógica:**
    1.  **Verificar Asignatura y Pertenencia:** Primero recupera la `Asignatura` por su ID. Lanza una `NotFoundException` si la asignatura no existe y una `UnauthorizedException` si el `id_docente` de la asignatura no coincide con el ID del docente que intenta abrir la sesión.
    2.  **Verificar Horario:** Comprueba si la asignatura está realmente programada para el `id_horario` dado llamando a `existe_clase_programada` en el repositorio.
    3.  **Comprobar Sesión Activa:** Evita la apertura de sesiones duplicadas comprobando si ya existe una sesión `EnProgreso` para la misma asignatura y horario.
    4.  **Crear Sesión:** Si todas las validaciones pasan, crea un DTO `SesionDeClaseCreate` y utiliza el `sesion_repository` para crear el nuevo registro de sesión, incluyendo el `tema` opcional.
*   **Retorna:** La entidad de dominio `SesionDeClase` recién creada.

---

### `CerrarSesionUseCase.py`

**Propósito:** Contiene la lógica para que un docente cierre una sesión de clase activa.

**Dependencias:**
*   `ISesionDeClaseRepository`: Para actualizar el estado de la sesión.
*   `IAsignaturaRepository`: Para verificar que el docente es el propietario de la asignatura de la sesión.

**Método `execute`:**
*   **Parámetros:** `id_sesion`, `id_docente`.
*   **Lógica:**
    1.  **Verificar Sesión:** Recupera la sesión por su ID.
    2.  **Verificar Pertenencia:** Obtiene la `Asignatura` asociada para asegurar que el `id_docente` coincide con el que intenta cerrar la sesión, previniendo acciones no autorizadas.
    3.  **Comprobar Estado:** Asegura que la sesión esté actualmente `EnProgreso`. Una sesión que ya está cerrada o en otro estado no puede ser cerrada de nuevo.
    4.  **Cerrar Sesión:** Crea un DTO `SesionDeClaseUpdate` para establecer el estado a `CERRADA` y registra la hora actual como `hora_fin`. Luego llama al método `update` en el repositorio.
*   **Retorna:** La entidad `SesionDeClase` actualizada, ahora marcada como cerrada.

---

### `CrearUsuarioUseCase.py`

**Propósito:** Gestiona la creación de un nuevo usuario, típicamente un docente.

**Dependencias:**
*   `IUsuarioRepository`: Para comprobar usuarios existentes y crear el nuevo.

**Método `execute`:**
*   **Parámetros:** `usuario_create` (un DTO `UsuarioCreate`).
*   **Lógica:**
    1.  **Comprobar Duplicados:** Verifica que no exista ningún usuario con el mismo correo electrónico para mantener la unicidad.
    2.  **Crear Usuario:** Llama al método `create` en el repositorio. La implementación del repositorio es responsable de operaciones sensibles a la seguridad como el hasheo de contraseñas.
*   **Retorna:** La entidad `Usuario` recién creada.

---

### `CrearEstudianteUseCase.py`

**Propósito:** Maneja la lógica de negocio para registrar un nuevo estudiante en el sistema.

**Dependencias:**
*   `IEstudianteRepository`: Para todas las operaciones de base de datos relacionadas con estudiantes.

**Método `execute`:**
*   **Parámetros:** `estudiante_create` (un DTO `EstudianteCreate`).
*   **Lógica:**
    1.  **Verificar Email:** Asegura que el correo electrónico del estudiante sea único en el sistema.
    2.  **Verificar RFC/UID:** Asegura que el identificador de la tarjeta NFC del estudiante (`rfc_uid`) también sea único para evitar duplicados.
    3.  **Crear Estudiante:** Si los datos son únicos, procede a crear el nuevo registro de estudiante.
*   **Retorna:** La entidad `Estudiante` recién creada.

---

### `CrearAsignaturaUseCase.py`

**Propósito:** Encapsula la lógica para crear una nueva asignatura (`Asignatura`).

**Dependencias:**
*   `IAsignaturaRepository`: Para crear la nueva asignatura.
*   `IUsuarioRepository`: Para verificar la existencia del docente que se asigna a la asignatura.

**Método `execute`:**
*   **Parámetros:** `asignatura_create` (un DTO `AsignaturaCreate`).
*   **Lógica:**
    1.  **Verificar Docente:** Confirma que el `id_docente` proporcionado en el DTO corresponde a un usuario existente en la base de datos.
    2.  **Crear Asignatura:** Si el docente existe, crea la nueva asignatura.
*   **Retorna:** La entidad `Asignatura` recién creada.

---

### `CrearHorarioUseCase.py`

**Propósito:** Gestiona la creación de un nuevo horario (`Horario`).

**Dependencias:**
*   `IHorarioRepository`: Para persistir el nuevo horario.

**Método `execute`:**
*   **Parámetros:** `horario_create` (un DTO `HorarioCreate`).
*   **Lógica:**
    1.  **Crear Horario:** Llama directamente al método `create` en el repositorio. Toda la validación de datos (por ejemplo, asegurar que `hora_fin` sea posterior a `hora_inicio`) se maneja dentro del propio DTO de Pydantic.
*   **Retorna:** La entidad `Horario` recién creada.

---

### `InscribirEstudianteUseCase.py`

**Propósito:** Maneja la lógica de inscribir a un estudiante en una asignatura, creando una entrada en la tabla de unión `Inscripcion`.

**Dependencias:**
*   `IAsignaturaRepository`: Para verificar que la asignatura existe.
*   `IEstudianteRepository`: Para verificar que el estudiante existe.
*   `IInscripcionRepository`: Para manejar la creación del registro de inscripción.

**Método `execute`:**
*   **Parámetros:** `id_asignatura`, `id_estudiante`.
*   **Lógica:**
    1.  **Verificar Asignatura y Estudiante:** Asegura que tanto la asignatura como el estudiante existan antes de intentar vincularlos.
    2.  **Comprobar Inscripción Existente:** Consulta el `inscripcion_repository` para evitar la creación de una inscripción duplicada.
    3.  **Crear Inscripción:** Si no existe una inscripción previa, crea un nuevo registro de `Inscripcion`.
*   **Retorna:** La entidad `Inscripcion` recién creada.

---

### `ProgramarClaseUseCase.py`

**Propósito:** Gestiona la programación de una asignatura en un horario específico, creando una entrada en la tabla de unión `ClaseProgramada`.

**Dependencias:**
*   `IAsignaturaRepository`: Para verificar que la asignatura existe.
*   `IHorarioRepository`: Para verificar que el horario existe.
*   `IClaseProgramadaRepository`: Para manejar la creación del registro de la clase programada.

**Método `execute`:**
*   **Parámetros:** `id_asignatura`, `id_horario`.
*   **Lógica:**
    1.  **Verificar Asignatura y Horario:** Asegura que tanto la asignatura como el horario existan.
    2.  **Comprobar Programación Existente:** Evita la programación duplicada comprobando si la asignatura ya está vinculada a ese horario.
    3.  **Crear Clase Programada:** Si la combinación es nueva, crea el registro de `ClaseProgramada`.
*   **Retorna:** La entidad `ClaseProgramada` recién creada.

---

### `RegistrarAsistenciaUseCase.py`

**Propósito:** Este es un caso de uso central que maneja la acción de "tap" de un estudiante para registrar su asistencia a una sesión de clase activa.

**Dependencias:**
*   `IRegistroAsistenciaRepository`: Para crear el registro de asistencia.
*   `ISesionDeClaseRepository`: Para encontrar la sesión activa.
*   `IEstudianteRepository`: Para identificar al estudiante a través de su UID de tarjeta NFC.
*   `IAsignaturaRepository`: Para verificar que el estudiante está inscrito en la asignatura.

**Método `execute`:**
*   **Parámetros:** `rfc_uid_estudiante`, `id_sesion`.
*   **Lógica:**
    1.  **Validar Estudiante:** Encuentra al estudiante basándose en su `rfc_uid`.
    2.  **Validar Sesión:** Encuentra la sesión de clase por su ID y asegura que esté `EnProgreso`.
    3.  **Validar Inscripción:** Comprueba si el estudiante identificado está realmente inscrito en la asignatura correspondiente a la sesión activa.
    4.  **Prevenir Duplicados:** Comprueba si el estudiante ya ha registrado su asistencia para esta sesión para asegurar la idempotencia (un estudiante no puede hacer "tap" dos veces).
    5.  **Determinar Estado:** Calcula el estado de la asistencia (`Presente` o `Tarde`) comparando la hora actual con la hora de inicio de la sesión más un margen de tolerancia definido en la configuración.
    6.  **Crear Registro:** Crea un DTO `RegistroAsistenciaCreate` con toda la información necesaria y llama al repositorio para guardar el registro de asistencia.
*   **Retorna:** La entidad `RegistroAsistencia` recién creada.
