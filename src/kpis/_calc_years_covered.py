
import logging

import pandas as pd

log = logging.getLogger(__name__)


def _calc_years_covered(df: pd.DataFrame) -> int:
    """
    Numero de anios distintos presentes en el DataFrame.

    Returns 0 si df esta vacio.
    """
    if df.empty:
        return 0
    return df["year"].nunique()

