# AutoAPI Builder

AutoAPI Builder es una herramienta de backend desarrollada en Python que permite generar automáticamente una API REST completa a partir de archivos `.json`. Ideal para prototipado rápido y mock de APIs.

---

## ¿Qué hace?
- Valida estructura de JSONs
- Genera resumen de campos y tipos
- Crea API REST con operaciones CRUD
- Funciona como base de datos temporal

---

## Instalación
**Requisito:** Python 3.8+

1. Clona el repositorio:
git clone https://github.com/mauroserralvodev/autoapi-builder.git
cd autoapi-builder
Entorno virtual y dependencias:

## Linux/macOS:

bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Windows:

bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
🚀 Cómo se usa
1. Validar JSON
bash
python cli.py validate examples/generation_logs.json
Verifica consistencia de estructura

## 2. Generar resumen
bash
python cli.py summary examples/generation_logs.json
Muestra campos, tipos y valores de ejemplo

## 3. Iniciar API
bash
python cli.py serve examples/generation_logs.json
Servidor disponible en http://127.0.0.1:8000

## Endpoints
http
GET /data → Lista todos los registros

GET /data/{campo}/{valor} → Búsqueda específica

POST /data → Añade nuevo registro (JSON body)

PUT /data/{campo}/{valor} → Actualiza registro

DELETE /data/{campo}/{valor} → Elimina registro

## Estructura del proyecto
autoapi-builder/

├── cli.py                # Interfaz CLI

├── storage.py            # Gestión de JSON

├── requirements.txt      # Dependencias

├── examples/             # Datos de ejemplo

│   └── invoices.json      # Ejemplo de JSON (para poder hacer pruebas)

└── README.md             # Este archivo

## Dependencias principales
FastAPI: Framework API modernas

Uvicorn: Servidor ASGI

Typer: Sistema CLI

Pydantic: Validación de datos

## Roadmap
Soporte múltiples colecciones

Autenticación por token

Exportación Swagger/OpenAPI

Modo read-only

Interfaz web explorador

## Desarrollado por @mauroserralvodev

