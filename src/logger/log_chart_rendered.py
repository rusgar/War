#src/logger/log_chart_rendered.py

import logging
from pathlib import Path

# Configuración global definida en el módulo
LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def log_chart_rendered(log: logging.Logger, chart_name: str, rows: int) -> None:
    """Registra el renderizado de gráficos (nivel DEBUG).[cite: 2]"""
    log.debug("CHART_RENDERED | chart=%s | rows_used=%d", chart_name, rows)
