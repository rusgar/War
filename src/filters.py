"""
filters.py
=========
Modulo de filtros del sidebar de Streamlit.

RAMA:    feature/ui
TAREA:   Implementar render_sidebar() y apply_filters().

Reglas:
- apply_filters() es una funcion pura (testeable sin Streamlit).
- render_sidebar() contiene solo UI (no se testea directamente).
- Llamar log_filter_applied() de logger.py al aplicar filtros.
- Cobertura minima: 80% en apply_filters y funciones auxiliares.

Commits de referencia:
  feat(filters): implement render_sidebar year slider and multiselects
  feat(filters): implement apply_filters with all filter types
  feat(filters): integrate log_filter_applied in apply_filters
  test(filters): add apply_filters full test suite
  docs(filters): update filters.md
"""

import logging

import pandas as pd
import streamlit as st

from src.logger.log_filter_applied import log_filter_applied

log = logging.getLogger(__name__)


def render_sidebar(df: pd.DataFrame) -> dict:
    """
    Renderiza el sidebar y devuelve los filtros seleccionados.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame original para extraer los valores unicos de cada filtro.

    Returns
    -------
    dict
        Claves: year_range (tuple|None), citizenship (list),
                gender (list), region (list), killed_by (list).
    """
    st.sidebar.title("Filtros")
    st.sidebar.markdown("---")

    # TODO (Paso 1): Slider de anio
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    year_range = st.sidebar.slider("Rango de anos", min_year, max_year, (min_year, max_year))

    st.sidebar.markdown("---")

    # TODO (Paso 2): Multiselect ciudadania
    citizenship = st.sidebar.multiselect(
        "Ciudadania",
        sorted(df["citizenship"].dropna().unique())
    )

    # TODO (Paso 3): Multiselect genero
    gender = st.sidebar.multiselect(
        "Genero",
        sorted(df["gender"].dropna().unique())
    )

    # TODO (Paso 4): Multiselect region
    region = st.sidebar.multiselect(
        "Region",
        sorted(df["event_location_region"].dropna().unique())
    )

    # TODO (Paso 5): Multiselect killed_by
    killed_by = st.sidebar.multiselect(
        "Causa de muerte",
        sorted(df["killed_by"].dropna().unique())
    )

    return {
        "year_range": year_range,
        "citizenship": citizenship,
        "gender": gender,
        "region": region,
        "killed_by": killed_by,
    }


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
