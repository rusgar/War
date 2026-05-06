from pathlib import Path


# Configuración global de logs definida en el módulo

LOG_DIR = Path("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

CHART_LOGGERS = {}

# Configuración global de data definida en el módulo

DATA_PATH = Path(__file__).parent.parent / "./data/fatalities.csv"