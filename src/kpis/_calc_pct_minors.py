
import logging

import pandas as pd

log = logging.getLogger(__name__)


def _calc_pct_minors(df: pd.DataFrame) -> float:
    """
    Porcentaje de victimas con edad < 18.

    Parameters
    ----------
    df : pd.DataFrame
        Necesita columna "age" numerica.

    Returns
    -------
    float
        Valor entre 0.0 y 100.0. Devuelve 0.0 si df esta vacio.

    Example
    -------
    >>> df = pd.DataFrame({"age": [10, 20, 30]})
    >>> round(_calc_pct_minors(df), 2)
    33.33
    """
    if df.empty:
        return 0.0
    minors = (df["age"] < 18).sum()
    return (minors / len(df)) * 100

