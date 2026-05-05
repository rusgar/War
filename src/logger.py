#src/logger.py

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path

# Configuración global definida en el módulo
LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


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

    # (Paso 2): Crear un StreamHandler para la consola 
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
   

   # (Paso 3): Si log_to_file es True, configurar archivo
    # --- Configuración de Archivo ---
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


def log_data_loaded(log: logging.Logger, n_rows: int, path: str) -> None:
    """Registra el evento de carga de datos de forma estructurada.[cite: 2]"""
    log.info("DATA_LOADED | rows=%d | path=%s", n_rows, path)


def log_filter_applied(log: logging.Logger, filters: dict, rows_before: int, rows_after: int) -> None:
    """Registra cuando se aplican filtros y el impacto en los datos.[cite: 2]"""
    log.info("FILTER_APPLIED | before=%d | after=%d | filters=%s", 
             rows_before, rows_after, filters)


def log_chart_rendered(log: logging.Logger, chart_name: str, rows: int) -> None:
    """Registra el renderizado de gráficos (nivel DEBUG).[cite: 2]"""
    log.debug("CHART_RENDERED | chart=%s | rows_used=%d", chart_name, rows)
