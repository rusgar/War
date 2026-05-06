#src/logger/setup_chart_logger.py

import logging

from src.config import CHART_LOGGERS, DATE_FORMAT, LOG_DIR, LOG_FORMAT

def setup_chart_logger(chart_name: str) -> logging.Logger:
    if chart_name in CHART_LOGGERS:
        return CHART_LOGGERS[chart_name]
    
    logger = logging.getLogger(chart_name)
    logger.setLevel(logging.INFO)
    logger.handlers = []
    
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{chart_name}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    CHART_LOGGERS[chart_name] = logger
    return logger

