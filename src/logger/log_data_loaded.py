#src/logger/log_data_loaded.py

import logging
from pathlib import Path

# Configuración global definida en el módulo
LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def log_data_loaded(log: logging.Logger, n_rows: int, path: str) -> None:
    """Registra el evento de carga de datos de forma estructurada.[cite: 2]"""
    log.info("DATA_LOADED | rows=%d | path=%s", n_rows, path)

