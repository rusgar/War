#src/logger/get_chart_logger.py

import logging

from src.logger.setup_chart_logger import setup_chart_logger


def get_chart_logger(chart_name: str) -> logging.Logger:
    return setup_chart_logger(chart_name)