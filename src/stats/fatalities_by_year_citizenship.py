#src/stats/fatalities_by_year_citizenship.py

import logging
from pathlib import Path
import pandas as pd

log = logging.getLogger(__name__)

RESULTS_DIR = Path("results")


def fatalities_by_year_citizenship(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla pivot: filas = año, columnas = ciudadanía.[cite: 4]"""
    pivot = df.pivot_table(
        index="year", 
        columns="citizenship", 
        aggfunc="size", 
        fill_value=0
    )
    # Añadir columna "Total" por fila[cite: 4]
    pivot["Total"] = pivot.sum(axis=1)
    return pivot

