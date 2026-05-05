#src/data_loader/_add_derived_features.py

import logging
import pandas as pd

# El logger se configura desde logger.py - aqui solo lo obtenemos
log = logging.getLogger(__name__)


def _add_derived_features(df: pd.DataFrame) -> pd.DataFrame: 
    """Genera columnas calculadas (Year, Month, Age Groups)."""

    # Extraer componentes de fecha
    df["year"] = df["date_of_event"].dt.year.astype("Int32")
    df["month"] = df["date_of_event"].dt.month.astype("Int32")
    df["month_name"] = df["date_of_event"].dt.strftime("%b")

        # Clasificación por grupos
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 17, 29, 44, 59, 120],
        labels=["Minor (0-17)", "Young (18-29)", "Adult (30-44)", "Middle (45-59)", "Senior (60+)"],
        right=True,
    )

    return df