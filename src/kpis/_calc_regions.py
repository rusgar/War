
import logging

import pandas as pd

log = logging.getLogger(__name__)


def _calc_regions(df: pd.DataFrame) -> int:
    """
    Numero de regiones distintas en event_location_region.

    Returns 0 si df esta vacio.
    """
    if df.empty:
        return 0
    return df["event_location_region"].nunique()

