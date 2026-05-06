#src/logger/log_chart_rendered.py

import logging


def log_chart_rendered(log: logging.Logger, chart_name: str, rows: int, progress: int = None) -> None:
    if progress is not None:
        log.info("CHART_RENDERED | chart=%s | rows_used=%d | progress=%d%%", chart_name, rows, progress)
    else:
        log.info("CHART_RENDERED | chart=%s | rows_used=%d", chart_name, rows)