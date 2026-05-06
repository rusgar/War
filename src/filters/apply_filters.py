import logging

import pandas as pd
import streamlit as st

from src.logger.log_filter_applied import log_filter_applied

log = logging.getLogger(__name__)

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Aplica los filtros al DataFrame. Funcion pura, sin efectos laterales.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame original.
    filters : dict
        Diccionario de filtros devuelto por render_sidebar().

    Returns
    -------
    pd.DataFrame
        Copia filtrada del DataFrame original.

    Notes
    -----
    - year_range None -> no filtrar por anio.
    - Lista vacia [] -> no filtrar por esa columna.
    - Llamar log_filter_applied() al final si el log esta disponible.
    """
    filtered = df.copy()

    # TODO (Paso 6): filtrar por year_range con .between()
    if filters["year_range"] is not None:
        filtered = filtered[
            filtered["year"].between(filters["year_range"][0], filters["year_range"][1])
        ]

    # TODO (Paso 7): filtrar por citizenship con .isin()
    if filters["citizenship"]:
        filtered = filtered[filtered["citizenship"].isin(filters["citizenship"])]

    # TODO (Paso 8): filtrar por gender
    if filters["gender"]:
        filtered = filtered[filtered["gender"].isin(filters["gender"])]

    # TODO (Paso 9): filtrar por region
    if filters["region"]:
        filtered = filtered[filtered["event_location_region"].isin(filters["region"])]

    # TODO (Paso 10): filtrar por killed_by
    if filters["killed_by"]:
        filtered = filtered[filtered["killed_by"].isin(filters["killed_by"])]

    # TODO (Paso 11): llamar log_filter_applied(log, filters, len(df), len(filtered))
    log_filter_applied(log, filters, len(df), len(filtered))

    return filtered
