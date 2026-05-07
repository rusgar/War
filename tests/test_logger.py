import logging
import pytest
from pathlib import Path
from src.config import LOG_DIR
from src.logger.setup_logger import setup_logger
from src.logger.log_data_loaded import log_data_loaded
from src.logger.log_filter_applied import log_filter_applied

@pytest.fixture(autouse=True)
def reset_logging():
    """
    Limpia los handlers de los loggers después de cada test para 
    evitar interferencias entre pruebas.
    """
    yield
    logger = logging.getLogger("test_logger")
    logger.handlers = []

def test_setup_logger_creation():
    """Verifica que el logger se cree con el nombre y nivel correctos."""
    name = "test_logger"
    logger = setup_logger(name=name, level=logging.DEBUG, log_to_file=False)
    
    assert logger.name == name
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) >= 1  # Al menos el StreamHandler

def test_setup_logger_file_creation(tmp_path):
    """
    Verifica que se cree el archivo de log si log_to_file es True.
    Nota: Se usa un nombre único para evitar colisiones.
    """
    logger_name = "file_test_logger"
    # Llamamos a la función
    setup_logger(name=logger_name, log_to_file=True)
    
    # Verificar que el directorio y el archivo existen
    assert LOG_DIR.exists()
    log_files = list(LOG_DIR.glob(f"{logger_name}_*.log"))
    assert len(log_files) > 0

def test_log_data_loaded(caplog):
    """Verifica el formato del mensaje en log_data_loaded."""
    logger = logging.getLogger("test_logger")
    with caplog.at_level(logging.INFO):
        log_data_loaded(logger, n_rows=100, path="data.csv")
    
    assert "DATA_LOADED | rows=100 | path=data.csv" in caplog.text

def test_log_filter_applied(caplog):
    """Verifica el formato del mensaje en log_filter_applied[cite: 2]."""
    logger = logging.getLogger("test_logger")
    filters = {"year": 2023}
    
    with caplog.at_level(logging.INFO):
        log_filter_applied(logger, filters, rows_before=50, rows_after=10)
    
    assert "FILTER_APPLIED | before=50 | after=10 | filters={'year': 2023}" in caplog.text

def test_prevent_duplicate_handlers():
    """Verifica que no se dupliquen handlers si se llama dos veces a setup_logger."""
    name = "duplicate_test"
    logger = setup_logger(name=name)
    initial_handlers = len(logger.handlers)
    
    # Segunda llamada
    logger = setup_logger(name=name)
    assert len(logger.handlers) == initial_handlers