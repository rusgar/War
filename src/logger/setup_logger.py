#src/logger.py

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path

from src.config import DATE_FORMAT, LOG_DIR, LOG_FORMAT


def setup_logger(
    name: str = "dashboard",
    level: int = logging.INFO,
    log_to_file: bool = True,
) -> logging.Logger:
    """
    Configura y devuelve el logger principal de la aplicacion.
    """

    # (Paso 1): Debes asignar el valor a la variable 'logger' 
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formateador común para todos los handlers[cite: 3]
    # Al definirlo así, el editor ya "detecta" la variable formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    
    # Evitar duplicar handlers si se llama varias veces a la función
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
   
        if log_to_file:
            try:
                # Crear LOG_DIR si no existe 
                LOG_DIR.mkdir(parents=True, exist_ok=True)

                # - Nombrar el fichero: dashboard_YYYYMMDD.log 
                today = datetime.now().strftime("%Y%m%d")
                log_file = LOG_DIR / f"{name}_{today}.log" 

                # Crear logging.FileHandler
                file_handler = logging.FileHandler(log_file, encoding="utf-8") 
                file_handler.setFormatter(formatter)

                # Añadir handler de archivo
                logger.addHandler(file_handler)

                # # (Paso 4 continuación): Añadir handler de consola y devolver[cite: 2]
                # logger.addHandler(console_handler)
            except Exception as e:
                # Si falla la creación del archivo, al menos lo notificamos en consola
                print(f"Error al configurar el archivo de log: {e}")
    
    return logger

