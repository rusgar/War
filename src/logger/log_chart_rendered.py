#src/logger/log_chart_rendered.py

import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def log_chart_rendered(log: logging.Logger, chart_name: str, rows: int, rows_rendered: int = None) -> None:
    """Registra el renderizado de gráficos (nivel DEBUG)."""
    if rows_rendered is not None:
        log.debug("CHART_RENDERED | chart=%s | rows_used=%d | rows_rendered=%d", chart_name, rows, rows_rendered)
    else:
        log.debug("CHART_RENDERED | chart=%s | rows_used=%d", chart_name, rows)


# def get_chart_logger(name: str = "charts") -> logging.Logger:
#     """Crea y devuelve un logger específico para gráficos."""
#     logger = logging.getLogger(name)
#     if not logger.handlers:
#         logger.setLevel(logging.DEBUG)
#         formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(formatter)
#         logger.addHandler(console_handler)
#     return logger