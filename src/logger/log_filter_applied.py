#src/logger/log_filter_applied.py

import logging
from pathlib import Path

# Configuración global definida en el módulo
LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def log_filter_applied(log: logging.Logger, filters: dict, rows_before: int, rows_after: int) -> None:
    """Registra cuando se aplican filtros y el impacto en los datos.[cite: 2]"""
    log.info("FILTER_APPLIED | before=%d | after=%d | filters=%s", 
             rows_before, rows_after, filters)