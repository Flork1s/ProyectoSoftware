ProyectoSoftware

Sistema de gestión para ensamblajes de PC (PC Builder) — API + Frontend con FastAPI, SQLModel y Cloudinary.

Descripción

ProyectoSoftware es una aplicación web construida con FastAPI que permite gestionar usuarios, componentes de hardware y configuraciones personalizadas de PCs. Incluye operaciones CRUD completas, renderizado de templates HTML, manejo de archivos estáticos y carga de imágenes mediante Cloudinary.

El proyecto implementa una arquitectura modular basada en routers, controladores y modelos ORM utilizando SQLModel, garantizando un desarrollo escalable y mantenible.

Estructura del proyecto
/router                # Rutas del sistema (users, builds, components, upload)
/services              # Lógica de negocio (si aplica)
/static                # CSS, JS, imágenes
/templates             # Plantillas HTML con Jinja2
config.py              # Configuración de Cloudinary
database.py / .db      # Base de datos y creación de tablas
main.py                # Punto de entrada de FastAPI
models.py              # Modelos SQLModel (Usuarios, Builds, Componentes, etc.)
requirements.txt       # Dependencias del proyecto


Al iniciar la aplicación se ejecuta:

Creación automática de tablas

Configuración de Cloudinary

Funcionalidades principales
Gestión de Usuarios

Crear, listar y administrar usuarios

Relación directa con sus builds

Gestión de Builds (ensamblajes)

Cada usuario puede tener múltiples builds

Cada build tiene:

Componentes asociados

Configuración (OS, BIOS, etc.)

Precio total calculado automáticamente

Gestión de Componentes

CRUD de componentes
| Relación                 | Tipo | Descripción                                                   |
|--------------------------|------|---------------------------------------------------------------|
| User → Build            | 1:N  | Un usuario puede tener múltiples builds registrados.          |
| Build ↔ Component       | N:M  | Un build contiene varios componentes y un componente puede pertenecer a varios builds. |
| Component ↔ Category    | N:M  | Un componente puede pertenecer a múltiples categorías.         |
| Build → Configuration   | 1:1  | Cada build tiene una configuración única (OS, BIOS, etc.).     |
**Mapa endpoints**
| Método | Endpoint        | Descripción                       | Parámetros          | Ejemplo        |
|--------|------------------|-----------------------------------|----------------------|----------------|
| GET    | /users          | Obtiene todos los usuarios        | —                    | /users         |
| GET    | /users/{id}     | Consulta un usuario por ID        | id: int              | /users/3       |
| POST   | /users          | Crea un nuevo usuario             | JSON (name, email)   | —              |
| PUT    | /users/{id}     | Actualiza un usuario completo     | id: int + JSON       | /users/2       |
| DELETE | /users/{id}     | Elimina un usuario                | id: int              | /users/4       |

| Método | Endpoint            | Descripción                           | Parámetros          | Ejemplo          |
|--------|----------------------|---------------------------------------|----------------------|------------------|
| GET    | /components         | Lista todos los componentes           | —                    | /components      |
| GET    | /components/{id}    | Consulta un componente por ID         | id: int              | /components/5    |
| POST   | /components         | Crea un nuevo componente              | JSON (name, kind, brand, price) | — |
| PUT    | /components/{id}    | Actualiza completamente un componente | id: int + JSON       | /components/2    |
| DELETE | /components/{id}    | Elimina un componente                 | id: int              | /components/8    |

| Método | Endpoint        | Descripción                       | Parámetros          | Ejemplo         |
|--------|------------------|-----------------------------------|----------------------|-----------------|
| GET    | /builds         | Obtiene todos los builds          | —                    | /builds         |
| GET    | /builds/{id}    | Consulta un build por ID          | id: int              | /builds/1       |
| POST   | /builds         | Crea un nuevo build               | JSON (name, user_id) | —               |
| PUT    | /builds/{id}    | Actualiza un build completo       | id: int + JSON       | /builds/4       |
| DELETE | /builds/{id}    | Elimina un build                  | id: int              | /builds/7       |

| Método | Endpoint                        | Descripción                           | Parámetros     | Ejemplo                        |
|--------|----------------------------------|-----------------------------------------|----------------|---------------------------------|
| GET    | /builds/{id}/configuration       | Consulta la configuración del build     | id: int        | /builds/3/configuration         |
| POST   | /builds/{id}/configuration       | Crea configuración del build            | id: int + JSON | —                               |
| PUT    | /configuration/{id}              | Actualiza la configuración              | id: int + JSON | /configuration/1                |

| Método | Endpoint        | Descripción                | Parámetros                 | Ejemplo           |
|--------|------------------|----------------------------|-----------------------------|--------------------|
| POST   | /upload/image   | Sube una imagen a la nube | file: multipart/form-data   | /upload/image     |

Categorías de Componentes

Organización por tipo de hardware

Relación flexible Component ↔ Category

Subida de Imágenes con Cloudinary

Configuración automática al iniciar el servidor

Endpoint dedicado para carga de imágenes

Compatible con JPG/PNG y manejo de URL

Plantillas HTML

Renderizado mediante Jinja2

Vistas dinámicas (home, errores, etc.)

Instalación y ejecución
1. Clonar el repositorio
git clone https://github.com/Flork1s/ProyectoSoftware.git
cd ProyectoSoftware

2. Crear entorno virtual
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

3. Instalar dependencias
pip install -r requirements.txt

4. Configurar variables de entorno

Crea un archivo .env con la configuración de Cloudinary:

CLOUDINARY_CLOUD_NAME=tu_cloud
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret


Si usas Render, agrega también:

RENDER_EXTERNAL_URL=https://<tu-app>.onrender.com

5. Ejecutar el servidor
uvicorn main:app --reload

Endpoints principales
Usuarios
GET /users
POST /users

Builds
GET /builds
POST /builds
PUT /builds/{id}

Componentes
GET /components
POST /components

Upload (Cloudinary)
POST /upload/image

Base de datos

El proyecto utiliza SQLModel (SQLAlchemy + Pydantic) con SQLite por defecto.
Las tablas se crean automáticamente en el inicio del servidor.

Entidades principales:

User

Build

Component

Category

Configuration

Tablas pivote:

BuildComponentLink

ComponentCategoryLink

Relaciones:

User → Build (1:N)

Build ↔ Component (N:N)

Component ↔ Category (N:N)

Build ↔ Configuration (1:1)

Cloudinary

Integrado mediante la librería cloudinary para subir imágenes.

Configuración centralizada en config.py

Soporte para subida y almacenamiento de imágenes

URL generada automáticamente desde Cloudinary

Tecnologías utilizadas

Python 3

FastAPI

SQLModel / SQLAlchemy

Uvicorn

Jinja2 (HTML templates)

Cloudinary

httpx (keep-alive)

Render (deployment)

Arquitectura del proyecto

API modular mediante routers

Modelos ORM con SQLModel

Templates renderizados mediante Jinja2

Manejo de archivos estáticos

Relaciones complejas entre entidades

Servicio de keep-alive para Render

Autor

Flork1s
Proyecto académico/desarrollo personal de software.
