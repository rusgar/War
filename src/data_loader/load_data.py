#src/data_loader/load_data.py

import logging
import pandas as pd
from pathlib import Path

from src.config import DATA_PATH

from src.data_loader._add_derived_features import _add_derived_features
from src.data_loader._apply_type_conversions import _apply_type_conversions
from src.data_loader._normalize_columns import _normalize_columns 

# El logger se configura desde logger.py - aqui solo lo obtenemos
log = logging.getLogger(__name__)

# Ruta por defecto


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """
    Orquestador de la carga y limpieza del dataset.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset no encontrado en: {path}")

    log.info("Cargando dataset desde %s", path)
    df = pd.read_csv(path)
    log.info("Registros cargados: %d", len(df))

    # Pipeline de procesamiento
    df = (df.pipe(_normalize_columns)
            .pipe(_apply_type_conversions)
            .pipe(_add_derived_features))

    log.info("Dataset limpio. Columnas: %s", df.columns.tolist())
    return df