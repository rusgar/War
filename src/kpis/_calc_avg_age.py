
import logging

import pandas as pd

log = logging.getLogger(__name__)


def _calc_avg_age(df: pd.DataFrame) -> float:
    """
    Edad media, redondeada a 1 decimal. Devuelve 0.0 si no hay edades validas.
    """
    if df.empty:
        return 0.0
    valid_ages = df["age"].dropna()
    if valid_ages.empty:
        return 0.0
    return round(valid_ages.mean(), 1)

