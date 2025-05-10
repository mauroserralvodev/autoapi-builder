from fastapi import FastAPI, HTTPException
from api_generator import generate_api
from storage import Storage
import logging

# Configuración de logging para depuración
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Crear una instancia de FastAPI
app = FastAPI()

# Instancia de la clase Storage para manejar los datos
storage = Storage('data.json')

# Inicializar la API con los datos almacenados
try:
    generate_api(app, storage)
    logger.info("API generada exitosamente.")
except Exception as e:
    logger.error(f"Error al generar la API: {e}")
    raise HTTPException(status_code=500, detail="No se pudo generar la API.")

@app.get("/")
def read_root():
    """
    Endpoint raíz que muestra un mensaje de bienvenida.
    """
    return {"message": "AutoAPI Builder está funcionando correctamente."}

@app.on_event("startup")
async def load_data_on_startup():
    """
    Carga los datos al iniciar la aplicación.
    Este evento asegura que los datos estén disponibles antes de que la API comience a servir.
    """
    try:
        logger.info("Cargando datos desde el archivo de almacenamiento...")
        storage.load_data('data.json')
        logger.info("Datos cargados correctamente.")
    except Exception as e:
        logger.error(f"Error al cargar los datos: {e}")
        raise HTTPException(status_code=500, detail="Error al cargar los datos del almacenamiento.")
