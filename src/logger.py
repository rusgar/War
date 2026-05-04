import logging
import logging.handlers
from datetime import datetime
from pathlib import Path.

# Configuración global definida en el módulo
LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str = "dashboard",
    level: int = logging.INFO,
    log_to_file: bool = True,
) -> logging.Logger:
    """
    Configura y devuelve el logger principal de la aplicacion.

    Crea dos handlers:
      - StreamHandler: muestra logs en consola (nivel >= WARNING en prod).
      - FileHandler: guarda todos los logs en logs/dashboard_YYYYMMDD.log.

    Parameters
    ----------
    name : str
        Nombre del logger raiz de la aplicacion.
    level : int
        Nivel minimo de logging (logging.DEBUG, INFO, WARNING...).
    log_to_file : bool
        Si True, tambien guarda logs en fichero.

    Returns
    -------
    logging.Logger
        Logger configurado listo para usar.

    Example
    -------
    >>> log = setup_logger()
    >>> log.info("App iniciada")
    """
    # (Paso 1): Crear el logger con 
    logging.getLogger(name)
    logger.setLevel(level)

    # TODO (Paso 2): Crear un StreamHandler con el formato LOG_FORMAT
    # Hint: logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # TODO (Paso 3): Si log_to_file es True:
    # - Crear LOG_DIR si no existe (LOG_DIR.mkdir(parents=True, exist_ok=True))
    # - Nombrar el fichero: dashboard_YYYYMMDD.log con la fecha de hoy
    # - Usar logging.FileHandler(ruta, encoding="utf-8")
    # - Anadir el mismo formato

    # TODO (Paso 4): Anadir los handlers al logger y devolver el logger

    raise NotImplementedError("setup_logger pendiente de implementar")


def log_data_loaded(log: logging.Logger, n_rows: int, path: str) -> None:
    """
    Registra el evento de carga de datos.

    Parameters
    ----------
    log : logging.Logger
    n_rows : int
        Numero de filas cargadas.
    path : str
        Ruta del archivo cargado.
    """
    # TODO: log.info con mensaje estructurado
    # Ejemplo: "DATA_LOADED | rows=%d | path=%s"
    raise NotImplementedError("log_data_loaded pendiente")


def log_filter_applied(log: logging.Logger, filters: dict, rows_before: int, rows_after: int) -> None:
    """
    Registra cuando se aplican filtros y cuantas filas resultan.

    Parameters
    ----------
    log : logging.Logger
    filters : dict
        Diccionario de filtros activos.
    rows_before : int
    rows_after : int
    """
    # TODO: log.info con mensaje estructurado
    # Ejemplo: "FILTER_APPLIED | before=%d | after=%d | filters=%s"
    raise NotImplementedError("log_filter_applied pendiente")


def log_chart_rendered(log: logging.Logger, chart_name: str, rows: int) -> None:
    """
    Registra cuando se renderiza un grafico.

    Parameters
    ----------
    log : logging.Logger
    chart_name : str
        Nombre de la funcion de grafico (ej. "chart_fatalities_over_time").
    rows : int
        Numero de filas del DataFrame usado.
    """
    # TODO: log.debug con mensaje estructurado
    raise NotImplementedError("log_chart_rendered pendiente")
