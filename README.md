# Blog Platform API

API RESTful sencilla para una plataforma de blogging construida con **FastAPI**, **MySQL** y **aiomysql**.

## 🚀 Características

- 📝 **CRUD completo para posts:** Crear, leer (todos o por ID), actualizar y eliminar publicaciones.
- 🔍 **Búsqueda por términos:** Filtrado parcial en título, contenido o categoría (`GET /posts?term=...`).
- 🛡️ **Validación robusta:** Esquemas y modelos estrictos con Pydantic.
- ⚡ **Asíncrono:** Conexiones no bloqueantes a MySQL con `aiomysql`.
- 📚 **Documentación interactiva:** Generada automáticamente con Swagger UI y ReDoc.

## 📋 Requisitos

- Python >= 3.10
- MySQL >= 8.0
- Dependencias gestionadas con [`uv`](https://github.com/astral-sh/uv)

## ⚙️ Configuración del Entorno

Copia el archivo de ejemplo `.env.example` para crear tu entorno local `.env`:

```bash
cp .env.example .env
```

## 🛠️ Instalación

Clona el repositorio e instalalas dependencias con uv:

```bash
uv sync
```

## 🏃‍♂️ Ejecución
Para iniciar el servidor de desarrollo:

```bash
uv run fastapi dev src/blog_api/main.py
```

## 📌 Endpoints Principales

|Método|Endpoint|Descripción|
|------|--------|-----------|
|GET|/|Ruta de bienvenida (Home)|
|GET|/posts|Obtener todos los posts (admite ?term=texto)|
|GET|/posts/{id}|Obtener un post por su ID
|POST|/posts/new_post|Crear una nueva publicación|
|PUT|/posts/{id}|Actualizar un post existente por su ID|
|DELETE|/posts/{id}|Eliminar un post por su ID (devuelve 204 No Content)|

##  📖 Documentación de la API
Una vez en ejecución, puedes acceder a la documentación interactiva en:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc
