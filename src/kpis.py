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
    # TODO: implementar
    # Hint: cuidado con len(df) == 0
    raise NotImplementedError("_calc_pct_minors pendiente")


def _calc_years_covered(df: pd.DataFrame) -> int:
    """
    Numero de anios distintos presentes en el DataFrame.

    Returns 0 si df esta vacio.
    """
    # TODO: implementar
    raise NotImplementedError("_calc_years_covered pendiente")


def _calc_regions(df: pd.DataFrame) -> int:
    """
    Numero de regiones distintas en event_location_region.

    Returns 0 si df esta vacio.
    """
    # TODO: implementar
    raise NotImplementedError("_calc_regions pendiente")


def _calc_avg_age(df: pd.DataFrame) -> float:
    """
    Edad media, redondeada a 1 decimal. Devuelve 0.0 si no hay edades validas.
    """
    # TODO: implementar
    raise NotImplementedError("_calc_avg_age pendiente")


# ── Funcion principal de UI ───────────────────────────────────────────────────

def render_kpis(df: pd.DataFrame, df_original: pd.DataFrame) -> None:
    """
    Renderiza 5 KPIs en una fila horizontal en la cabecera del dashboard.

    KPIs mostrados:
      1. Total fatalidades  (delta vs total original)
      2. Edad promedio      (delta vs promedio original)
      3. % Menores de 18    (delta vs % original)
      4. Anos cubiertos
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
    # TODO (Paso 1): col1, col2, col3, col4, col5 = st.columns(5)

    # TODO (Paso 2): col1 -> Total fatalidades
    # st.metric("Total fatalidades", f"{len(df):,}",
    #           delta=len(df) - len(df_original))

    # TODO (Paso 3): col2 -> Edad promedio
    # Usar _calc_avg_age()

    # TODO (Paso 4): col3 -> % Menores de 18
    # Usar _calc_pct_minors(), formatear como "XX.X%"

    # TODO (Paso 5): col4 -> Anos cubiertos
    # Usar _calc_years_covered()

    # TODO (Paso 6): col5 -> Regiones
    # Usar _calc_regions()

    pass  # eliminar cuando este implementado
