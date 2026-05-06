
import logging

import pandas as pd
import streamlit as st

from src.kpis._calc_regions import _calc_regions
from src.kpis._calc_years_covered import _calc_years_covered
from src.kpis._calc_avg_age import _calc_avg_age
from src.kpis._calc_pct_minors import _calc_pct_minors

log = logging.getLogger(__name__)


def render_kpis(df: pd.DataFrame, df_original: pd.DataFrame) -> None:
    """
    Renderiza 5 KPIs en una fila horizontal en la cabecera del dashboard.

    KPIs mostrados:
      1. Total fatalidades  (delta vs total original)
      2. Edad promedio      (delta vs promedio original)
      3. % Menores de 18    (delta vs % original)
      4. Años cubiertos
      5. Regiones afectadas

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con filtros aplicados.
    df_original : pd.DataFrame
        DataFrame completo sin filtros (para calcular deltas).

    Notes
    -----
    - Usar st.columns(5).
    - Los deltas son: valor_filtrado - valor_original.
    - Para metricas donde un valor menor es mejor, usar delta_color="inverse".
    - Llamar las funciones _calc_*() que implementaste arriba.
    """
    col1, col2, col3, col4, col5 = st.columns(5)

    avg_age = _calc_avg_age(df)
    avg_age_original = _calc_avg_age(df_original)

    pct_minors = _calc_pct_minors(df)
    pct_minors_original = _calc_pct_minors(df_original)

    col1.metric(
        "Total fatalidades",
        f"{len(df):,}",
        delta=len(df) - len(df_original),
        delta_color="inverse"
    )

    col2.metric(
        "Edad promedio",
        f"{avg_age}",
        delta=avg_age - avg_age_original,
        delta_color="inverse"
    )

    col3.metric(
        "% Menores de 18",
        f"{pct_minors:.1f}%",
        delta=pct_minors - pct_minors_original,
        delta_color="inverse"
    )

    col4.metric(
        "Años cubiertos",
        _calc_years_covered(df)
    )

    col5.metric(
        "Regiones",
        _calc_regions(df)
    )
