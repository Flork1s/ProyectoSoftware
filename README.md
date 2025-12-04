# ProyectoSoftware

## 🧾 Descripción

**ProyectoSoftware** es una aplicación desarrollada para gestionar información mediante operaciones CRUD, utilizando una estructura organizada en rutas, servicios, plantillas HTML y archivos estáticos.  
El proyecto está diseñado para servir como base de un sistema web modular, escalable y fácil de mantener, utilizando Python como lenguaje principal y una arquitectura clara para manejar datos, vistas y lógica de negocio.

## Estructura del proyecto
/router ← Rutas del servidor / lógica de enrutamiento
/services ← Servicios / lógica de negocio
/static ← Archivos estáticos (CSS, JS, imágenes)
/templates ← Plantillas HTML
Kind.py
config.py
crud.py
database.db / database.py
main.py
models.py
requirements.txt

## Instalación / Cómo empezar

1. Clona el repositorio  
mkdir <nombre_archivo>
cd <nombre_archivo>
git clone https://github.com/Flork1s/ProyectoSoftware.git .

2. Entorno virtual
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

3. Instalar requerimientos
pip install -r requirements.txt

Tecnologías utilizadas

Python
FastApi
HTML / CSS (Jinja2)
Cloudinary
