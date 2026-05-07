#src/logger/log_data_loaded.py

import logging


def log_data_loaded(log: logging.Logger, n_rows: int, path: str) -> None:
    """Registra el evento de carga de datos de forma estructurada.[cite: 2]"""
    log.info("DATA_LOADED | rows=%d | path=%s", n_rows, path)

