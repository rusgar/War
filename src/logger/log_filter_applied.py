#src/logger/log_filter_applied.py

import logging


def log_filter_applied(log: logging.Logger, filters: dict, rows_before: int, rows_after: int) -> None:
    """Registra cuando se aplican filtros y el impacto en los datos.[cite: 2]"""
    log.info("FILTER_APPLIED | before=%d | after=%d | filters=%s", 
             rows_before, rows_after, filters)