import logging

import pandas as pd
import streamlit as st


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

