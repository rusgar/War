#src/data_loader/_normalize_columns.py

import logging
import pandas as pd

# El logger se configura desde logger.py - aqui solo lo obtenemos
log = logging.getLogger(__name__)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame: 
    """Normaliza los nombres de las columnas a snake_case.""" 
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df
