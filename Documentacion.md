# 📘 Documentación Técnica — ProyectoSoftware

## 1. Introducción
Este documento describe la arquitectura, el funcionamiento interno y las decisiones técnicas del proyecto **ProyectoSoftware**, una aplicación desarrollada en Python con una estructura modular diseñada para gestionar información mediante operaciones CRUD y presentar contenido dinámico a través de plantillas HTML.  
El objetivo principal es documentar cómo está construido el sistema para facilitar su mantenimiento, escalabilidad y comprensión por parte de nuevos desarrolladores.

---

## 2. Arquitectura General
El sistema está organizado siguiendo una arquitectura por capas:

- **Capa de rutas (router/)**: Maneja las solicitudes HTTP y las direcciona a la lógica correspondiente.  
- **Capa de servicios (services/)**: Contiene la lógica de negocio, validaciones y transformaciones de datos.  
- **Capa de datos**:  
  - `crud.py`: Funciones CRUD.  
  - `database.py`: Conexión y ejecución de queries.  
  - `models.py`: Definición de entidades.  
- **Capa de presentación**:  
  - `templates/`: Plantillas HTML.  
  - `static/`: Archivos CSS, JS e imágenes.

La aplicación principal se controla desde `main.py`, que inicializa la configuración, registra rutas y levanta el servidor.

---

## 3. Descripción de Módulos

### `main.py`
- Punto de entrada del sistema.
- Inicializa la aplicación y sus configuraciones.
- Registra las rutas ubicadas en `router/`.
- Ejecuta el servidor local.

### `config.py`
- Configuraciones globales del proyecto (constantes, variables, rutas base, etc.).

### `crud.py`
- Implementa las funciones para:
  - Crear registros.
  - Leer registros.
  - Actualizar registros.
  - Eliminar registros.
- Interactúa directamente con la base de datos.

### `database.py`
- Administra la conexión con la base de datos SQLite.
- Ejecuta consultas SQL.
- Maneja la creación de tablas si es necesario.

### `models.py`
- Define las clases o estructuras que representan las entidades del sistema.

### `Kind.py`
- Archivo asociado a funcionalidades específicas del proyecto (indicar propósito si es necesario).

### Directorio `/router/`
- Contiene los controladores que reciben y procesan peticiones del usuario.
- Cada archivo representa un grupo de rutas o funcionalidades específicas.

### Directorio `/services/`
- Aloja la lógica de negocio.
- Realiza validaciones y transformaciones de datos antes de enviarlos al CRUD.

### Directorio `/templates/`
- Contiene las plantillas HTML usadas para mostrar información.
- Las plantillas reciben datos dinámicos desde los controladores.

### Directorio `/static/`
Incluye recursos como:
- CSS
- JavaScript
- Imágenes
- Íconos

---
## 4. Flujo de Funcionamiento

### Flujo general de una operación CRUD

1. El usuario ejecuta una acción (ejemplo: enviar un formulario).
2. La solicitud llega a un controlador en `/router/`.
3. El router envía los datos a un servicio correspondiente en `/services/`.
4. El servicio valida o transforma la información.
5. El servicio llama a `crud.py` para realizar la operación en la BD.
6. `crud.py` usa `database.py` para ejecutar la consulta SQL.
7. Los datos regresan al controlador.
8. El controlador renderiza una plantilla HTML desde `/templates/`.

Este flujo asegura separación adecuada entre lógica, datos y presentación.

---

## 5. Dependencias

Las dependencias declaradas comúnmente incluyen:

- Python 3.x  
- Flask (si está siendo utilizado)  
- SQLite3  
- Jinja2  
- Otras librerías especificadas en `requirements.txt`

---

## 6. Requerimientos Funcionales

- RF01: El sistema debe permitir registrar nuevos datos.  
- RF02: El sistema debe permitir editar registros existentes.  
- RF03: El sistema debe permitir eliminar registros.  
- RF04: El sistema debe mostrar los registros almacenados.  
- RF05: Integración entre HTML y backend Python.

---

## 7. Requerimientos No Funcionales

- RNF01: El sistema debe tener una estructura modular.  
- RNF02: El proyecto debe ser fácil de mantener.  
- RNF03: Desempeño adecuado para cargas ligeras.  
- RNF04: Base de datos accesible sin configuración adicional.  
- RNF05: Escalabilidad para futuras funciones.

---

## 8. Decisiones Técnicas

- Se seleccionó **SQLite** por ser rápido, sencillo y sin servidor.  
- Estructura MVC para mejorar legibilidad, mantenimiento y escalabilidad.  
- Plantillas HTML para optimizar la reutilización de código visual.  
- Separación de responsabilidades entre rutas, servicios y datos.

---

## 9. Pruebas

### Pruebas manuales actuales
- Verificación del CRUD mediante formularios y pantallas del sistema.
- Revisión de logs y respuestas en la consola del servidor.

### Pruebas recomendadas a futuro
- Pruebas unitarias para funciones CRUD.  
- Testing de rutas (endpoints HTTP).  
- Validación automática de entradas.

##10. Arquitectura
main.py
│
├── router/
├── services/
├── templates/
├── static/
├── crud.py
├── database.py
└── models.py

##11. Diagrama UML
                          +---------------------+
                          |        Kind         |
                          |---------------------|
                          |  CPU                |
                          |  GPU                |
                          |  RAM                |
                          |  STORAGE            |
                          |  MOTHERBOARD        |
                          |  POWER_SUPPLY       |
                          |  COOLER             |
                          |  CASE               |
                          +---------------------+

+--------------------+        1      N       +--------------------+
|       User         |---------------------->|       Build        |
|--------------------|                       |--------------------|
| id : int (PK)      |<----------------------+ user : User        |
| name : str         |                       | name : str         |
| email : str        |                       | total_price: float |
| image_url : str?   |                       |--------------------|
|--------------------|                       | components: List   |
| builds: List<Build>|                       | configuration: Conf|
+--------------------+                       +--------------------+
                                                   |
                                                   | 1
                                                   | 
                                                   v
                                       +--------------------------+
                                       |     Configuration        |
                                       |--------------------------|
                                       | id : int (PK)            |
                                       | build_id : int (Unique)  |
                                       | os : str?                |
                                       | bios_version : str?      |
                                       +--------------------------+


      +--------------------+       N        M       +--------------------+
      |     Component      |<---------------------->|       Build        |
      |--------------------|    BuildComponentLink  |--------------------|
      | id : int (PK)      |----------------------->| id : int           |
      | name : str         | build_id : int (FK)    | name : str         |
      | kind : str/Kind    | component_id : int(FK) | user_id : int(FK)  |
      | brand : str        |                        +--------------------+
      | price : float      |
      |--------------------|
      | builds: List<Build>|
      | categories: List<Cat>|
      +--------------------+

                    M                             N
      +--------------------+   ComponentCategoryLink    +--------------------+
      |     Component      |--------------------------->|     Category       |
      |--------------------| component_id : int (FK)    |--------------------|
      | id : int (PK)      | category_id : int (FK)     | id : int (PK)      |
      | ...                |--------------------------->| name : str         |
      +--------------------+                            | components: List   |
                                                        +--------------------+
