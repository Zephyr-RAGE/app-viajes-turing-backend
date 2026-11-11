# Sistema de Cambio de Monedas – Backend

## 1. Descripción general

Backend de una aplicación de cambio de monedas desarrollado con FastAPI y PostgreSQL. El proyecto proporciona una API REST para gestionar usuarios, consultar información de monedas, países y ciudades, y administrar operaciones relacionadas con el historial del sistema.

La aplicación incorpora mecanismos de autenticación mediante JSON Web Tokens (JWT), renovación de sesiones, revocación de tokens y registro de eventos para facilitar el seguimiento y diagnóstico de las operaciones.

## 2. Tecnologías utilizadas

- **Python:** lenguaje principal.
- **FastAPI:** desarrollo de la API REST.
- **PostgreSQL:** sistema gestor de base de datos.
- **SQLAlchemy:** ORM para la interacción con la base de datos.
- **Alembic:** administración y control de migraciones.
- **Pydantic:** validación de datos y configuración.
- **Pydantic Settings:** gestión de variables de entorno.
- **PyJWT:** generación y validación de tokens JWT.
- **Uvicorn:** servidor ASGI.
- **Argon2:** mecanismo de protección de contraseñas.
- **Pytest:** framework para pruebas automatizadas.

## 3. Arquitectura del backend

El proyecto utiliza una arquitectura organizada por responsabilidades para separar la lógica de negocio, el acceso a datos, la validación y la exposición de endpoints.

### Componentes principales

- **Core:** configuración general, seguridad, dependencias y manejo de tokens.
- **Database:** conexión y administración de sesiones de base de datos.
- **Middleware:** procesamiento transversal de solicitudes, incluyendo identificación de trazas.
- **Models:** representación de las entidades de la base de datos.
- **Repositories:** operaciones de acceso y consulta de datos.
- **Routes:** definición de endpoints de la API.
- **Schemas:** validación y estructura de los datos de entrada y salida.
- **Services:** lógica de negocio y procesamiento de operaciones.

## 4. Estructura del proyecto

```text
backend-viajes/
├── app/
│   ├── core/
│   ├── database/
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── migrations/
│   └── versions/
├── logs/
├── tests/
├── alembic.ini
└── requirements.txt
```

## 5. Configuración del entorno

### Requisitos previos

- Python compatible con las dependencias del proyecto.
- PostgreSQL.
- Git.
- pip.

### Clonar el repositorio

```bash
git clone https://github.com/Zephyr-RAGE/app-viajes-turing-backend.git
cd app-viajes-turing-backend/backend-viajes
```

### Crear un entorno virtual

```bash
python -m venv venv
```

Activarlo en Windows:

```bash
venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## 6. Variables de entorno

La aplicación utiliza Pydantic Settings para cargar la configuración desde un archivo `.env`.

Crear un archivo `.env` en la raíz de `backend-viajes/` con la siguiente estructura:

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_contrasena
DB_NAME=nombre_base_datos
DB_HOST=localhost
DB_PORT=5432

APP_TOKEN_SECRET=generar_un_secreto_seguro
```

**Importante:** el archivo `.env` contiene información sensible y no debe publicarse en el repositorio. Cada entorno debe configurar sus propias credenciales.

## 7. Base de datos y migraciones

El proyecto utiliza PostgreSQL y SQLAlchemy para gestionar la persistencia de información.

Alembic permite mantener un historial de cambios en la estructura de la base de datos mediante migraciones versionadas.

Para aplicar las migraciones:

```bash
alembic upgrade head
```

Migraciones principales:

- `b70cbc149da7`: estructura inicial de la base de datos.
- `a5bcaddcc6de`: inserción de datos iniciales del catálogo.
- `817fedf5dc45`: incorporación de tablas para revocación y administración de tokens.

## 8. Autenticación y seguridad

El backend implementa autenticación basada en JWT para controlar el acceso a los recursos protegidos.

Entre los mecanismos desarrollados se encuentran:

- Generación de tokens de acceso.
- Generación y renovación de tokens de actualización (_refresh tokens_).
- Validación de tokens y sesiones.
- Revocación de tokens para impedir su reutilización.
- Protección de contraseñas mediante Argon2.
- Gestión de configuración sensible mediante variables de entorno.

## 9. Logs y trazabilidad

El sistema incorpora configuración de registros mediante el módulo de logging de Python.

También utiliza un middleware de identificación de solicitudes (_trace ID_), que permite asociar eventos de una misma petición y facilitar el seguimiento de operaciones y la investigación de errores.

Los registros locales no deben incluirse en el repositorio.

## 10. Ejecución del proyecto

Desde la carpeta `backend-viajes/`, con el entorno virtual activado y las variables de entorno configuradas:

```bash
uvicorn app.main:app --reload
```

La documentación interactiva de FastAPI estará disponible en:

```text
http://127.0.0.1:8000/docs
```

## 11. Consideraciones

- No publicar credenciales ni secretos.
- No subir el entorno virtual.
- Mantener las migraciones versionadas.
- Configurar las variables de entorno antes de iniciar la aplicación.
- Utilizar un secreto seguro para la firma y validación de tokens.
