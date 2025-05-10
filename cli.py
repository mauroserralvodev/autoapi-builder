import json
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import typer
from fastapi.responses import JSONResponse
from storage import Storage
from typing import Optional

# Configuración de logging para depuración y seguimiento
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Crear una aplicación FastAPI
app = FastAPI()

# Definir el modelo de datos para la validación y creación de registros
class Record(BaseModel):
    id: int
    name: str
    status: str
    value: float

# Crear una instancia de la clase Storage
storage = Storage('data.json')

# Inicializar Typer para la CLI
cli = typer.Typer()

@app.get("/data")
async def get_data():
    """Obtiene todos los registros de datos"""
    try:
        data = storage.get_all_data()
        return JSONResponse(content={"data": data})
    except Exception as e:
        logger.error(f"Error al obtener los datos: {e}")
        raise HTTPException(status_code=500, detail="No se pudo obtener los datos.")

@app.get("/data/{field}/{value}")
async def get_data_by_field(field: str, value: str):
    """Busca registros por un campo y valor específicos"""
    try:
        data = storage.search_data(field, value)
        if not data:
            raise HTTPException(status_code=404, detail="No se encontró el registro.")
        return JSONResponse(content={"data": data})
    except Exception as e:
        logger.error(f"Error al buscar los datos: {e}")
        raise HTTPException(status_code=500, detail="No se pudo realizar la búsqueda.")

@app.post("/data")
async def add_data(record: Record):
    """Añade un nuevo registro de datos"""
    try:
        storage.add_data(record.dict())
        return JSONResponse(status_code=201, content={"message": "Registro creado correctamente"})
    except Exception as e:
        logger.error(f"Error al agregar el registro: {e}")
        raise HTTPException(status_code=500, detail="No se pudo agregar el registro.")

@app.put("/data/{field}/{value}")
async def update_data(field: str, value: str, record: Record):
    """Actualiza un registro existente"""
    try:
        if not storage.update_data(field, value, record.dict()):
            raise HTTPException(status_code=404, detail="Registro no encontrado para actualizar.")
        return JSONResponse(content={"message": "Registro actualizado correctamente"})
    except Exception as e:
        logger.error(f"Error al actualizar el registro: {e}")
        raise HTTPException(status_code=500, detail="No se pudo actualizar el registro.")

@app.delete("/data/{field}/{value}")
async def delete_data(field: str, value: str):
    """Elimina un registro por campo y valor"""
    try:
        if not storage.delete_data(field, value):
            raise HTTPException(status_code=404, detail="Registro no encontrado para eliminar.")
        return JSONResponse(content={"message": "Registro eliminado correctamente"})
    except Exception as e:
        logger.error(f"Error al eliminar el registro: {e}")
        raise HTTPException(status_code=500, detail="No se pudo eliminar el registro.")

# Funciones de línea de comandos con Typer
@cli.command()
def validate(filename: str):
    """Valida un archivo JSON"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("El archivo JSON debe contener una lista de registros.")
            logger.info("Archivo JSON validado correctamente.")
            typer.echo("El archivo JSON es válido.")
    except ValueError as ve:
        logger.error(f"Error en el archivo JSON: {ve}")
        typer.echo(f"Error en el archivo JSON: {ve}")
    except Exception as e:
        logger.error(f"Error al leer el archivo JSON: {e}")
        typer.echo(f"Error al leer el archivo JSON: {e}")

@cli.command()
def summary(filename: str):
    """Genera un resumen del archivo JSON"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("El archivo JSON debe contener una lista de registros.")
            summary_data = {
                "fields": list(data[0].keys()) if data else [],
                "count": len(data)
            }
            logger.info(f"Resumen del archivo JSON: {summary_data}")
            typer.echo(json.dumps(summary_data, indent=2))
    except ValueError as ve:
        logger.error(f"Error en el archivo JSON: {ve}")
        typer.echo(f"Error en el archivo JSON: {ve}")
    except Exception as e:
        logger.error(f"Error al leer el archivo JSON: {e}")
        typer.echo(f"Error al leer el archivo JSON: {e}")

@cli.command()
def serve(filename: str):
    """Inicia un servidor FastAPI para servir los datos"""
    try:
        logger.info(f"Iniciando servidor con los datos del archivo {filename}")
        storage.load_data(filename)
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        logger.error(f"Error al iniciar el servidor: {e}")
        typer.echo(f"Error al iniciar el servidor: {e}")

# Comando principal
if __name__ == "__main__":
    cli()
