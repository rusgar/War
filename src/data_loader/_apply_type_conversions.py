#src/data_loader/_apply_type_conversions.py

import logging
import pandas as pd

# El logger se configura desde logger.py - aqui solo lo obtenemos
log = logging.getLogger(__name__)


def _apply_type_conversions(df: pd.DataFrame) -> pd.DataFrame: 
    """Aplica conversiones de tipos y limpieza de datos básicos."""
# Convertir fechas
    df["date_of_event"] = pd.to_datetime(df["date_of_event"], errors="coerce")
    df["date_of_death"] = pd.to_datetime(df["date_of_death"], errors="coerce")

# Limpiar edades
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["gender"] = df["gender"].map({"M": "Male", "F": "Female"}).fillna("Unknown") 

    return df
