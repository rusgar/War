#src/logger.py

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str = "dashboard",
    level: int = logging.INFO,
    log_to_file: bool = True,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_to_file:
            try:
                LOG_DIR.mkdir(parents=True, exist_ok=True)
                today = datetime.now().strftime("%Y%m%d")
                log_file = LOG_DIR / f"{name}_{today}.log"
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"Error al configurar el archivo de log: {e}")
    return logger


def log_data_loaded(log: logging.Logger, n_rows: int, path: str) -> None:
    log.info("DATA_LOADED | rows=%d | path=%s", n_rows, path)


def log_filter_applied(log: logging.Logger, filters: dict, rows_before: int, rows_after: int) -> None:
    log.info("FILTER_APPLIED | before=%d | after=%d | filters=%s", 
             rows_before, rows_after, filters)


def log_chart_rendered(log: logging.Logger, chart_name: str, rows: int) -> None:
    log.debug("CHART_RENDERED | chart=%s | rows_used=%d", chart_name, rows)