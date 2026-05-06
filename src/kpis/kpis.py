"""
kpis.py
=======
Modulo de metricas KPI para la cabecera del dashboard.

RAMA:    feature/ui
TAREA:   Implementar las funciones auxiliares y render_kpis().

Estrategia de testing:
- Las funciones _calc_*() son puras -> testarlas directamente.
- render_kpis() usa st.metric() -> mockearlo con unittest.mock.patch.
- Cobertura minima: 80%.

Commits de referencia:
  feat(kpis): add _calc_pct_minors helper function
  feat(kpis): add _calc_years_covered and _calc_regions helpers
  feat(kpis): implement render_kpis with st.columns and st.metric
  test(kpis): add unit tests for all _calc_* functions
  test(kpis): mock streamlit and verify metric call count
  docs(kpis): update kpis.md
"""

import logging

import pandas as pd
import streamlit as st

log = logging.getLogger(__name__)


# ── Funciones auxiliares (puras, testeables sin Streamlit) ────────────────────

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


def _calc_years_covered(df: pd.DataFrame) -> int:
    """
    Numero de anios distintos presentes en el DataFrame.

    Returns 0 si df esta vacio.
    """
    if df.empty:
        return 0
    return df["year"].nunique()


def _calc_regions(df: pd.DataFrame) -> int:
    """
    Numero de regiones distintas en event_location_region.

    Returns 0 si df esta vacio.
    """
    if df.empty:
        return 0
    return df["event_location_region"].nunique()


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


# ── Funcion principal de UI ───────────────────────────────────────────────────

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
