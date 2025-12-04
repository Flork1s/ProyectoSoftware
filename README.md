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

Tarea de keep-alive para evitar suspensión en Render

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

Relación muchos a muchos con builds

Relación muchos a muchos con categorías

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
