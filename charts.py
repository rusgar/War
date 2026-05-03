"""
charts.py
=========
Modulo de visualizaciones Plotly para el dashboard.

RAMA:    feature/visualization
TAREA:   Implementar todas las funciones marcadas con TODO.

Principios:
- Funciones PURAS: solo reciben DataFrame, devuelven go.Figure.
- Ningun import de streamlit aqui.
- Cada grafico loguea su render con log_chart_rendered() de logger.py.
- Cobertura minima: 80% de este modulo.

Commits de referencia:
  feat(charts): implement chart_fatalities_over_time
  feat(charts): implement chart_monthly_heatmap
  feat(charts): implement chart_age_distribution
  feat(charts): implement chart_gender_breakdown
  feat(charts): implement chart_by_region stacked bars
  feat(charts): implement chart_top_locations treemap
  feat(charts): implement chart_killed_by donut
  test(charts): add all chart tests
  docs(charts): update charts.md
"""

import logging

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

log = logging.getLogger(__name__)

# Paleta compartida — no modificar sin consenso del equipo
PALETTE = {
    "Palestinian": "#2196F3",
    "Israeli": "#FF9800",
    "Foreign": "#9C27B0",
}
MONTHS_ES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
             "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


# ── Grafico 1 ─────────────────────────────────────────────────────────────────

def chart_fatalities_over_time(df: pd.DataFrame) -> go.Figure:
    """
    Lineas: fatalidades por anio, una linea por ciudadania.

    Parameters
    ----------
    df : pd.DataFrame
        Columnas requeridas: year, citizenship.

    Returns
    -------
    go.Figure

    Hints
    -----
    - df.groupby(["year","citizenship"]).size().reset_index(name="total")
    - px.line(x="year", y="total", color="citizenship", color_discrete_map=PALETTE)
    - fig.update_layout(title="Fatalidades por Año")
    - Opcional: anotacion en el maximo de cada ciudadania
    - Llamar log_chart_rendered(log, "chart_fatalities_over_time", len(df))
      importando la funcion de logger.py
    """
    # TODO: implementar
    raise NotImplementedError("chart_fatalities_over_time pendiente")


# ── Grafico 2 ─────────────────────────────────────────────────────────────────

def chart_monthly_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Heatmap: eje X = mes (1-12), eje Y = anio, color = fatalidades.

    Parameters
    ----------
    df : pd.DataFrame
        Columnas requeridas: year, month.

    Returns
    -------
    go.Figure

    Hints
    -----
    - pivot = df.groupby(["year","month"]).size().unstack(fill_value=0)
    - go.Heatmap(z=pivot.values, x=MONTHS_ES, y=pivot.index, colorscale="YlOrRd")
    - fig.update_layout(title="Fatalidades por Mes y Año")
    """
    # TODO: implementar
    raise NotImplementedError("chart_monthly_heatmap pendiente")


# ── Grafico 3 ─────────────────────────────────────────────────────────────────

def chart_age_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Histograma de edades con marginal rug, por ciudadania.

    Parameters
    ----------
    df : pd.DataFrame
        Columnas requeridas: age, citizenship.

    Returns
    -------
    go.Figure

    Hints
    -----
    - Filtra: df[df["age"].between(0, 110)].copy()
    - px.histogram(nbins=40, marginal="rug", color="citizenship",
                   color_discrete_map=PALETTE, opacity=0.7)
    - Anadir linea vertical en la media: fig.add_vline(x=media, ...)
    - Titulo: "Distribucion de Edades"
    """
    # TODO: implementar
    raise NotImplementedError("chart_age_distribution pendiente")


# ── Grafico 4 ─────────────────────────────────────────────────────────────────

def chart_gender_breakdown(df: pd.DataFrame) -> go.Figure:
    """
    Sunburst de dos niveles: ciudadania -> genero.

    Parameters
    ----------
    df : pd.DataFrame
        Columnas requeridas: citizenship, gender.

    Returns
    -------
    go.Figure

    Hints
    -----
    - Agrupa por ["citizenship","gender"] y cuenta.
    - go.Sunburst(ids, labels, parents, values) construido manualmente
      o px.sunburst(path=["citizenship","gender"], values="count")
    - Titulo: "Distribucion por Ciudadania y Genero"
    """
    # TODO: implementar
    raise NotImplementedError("chart_gender_breakdown pendiente")


# ── Grafico 5 ─────────────────────────────────────────────────────────────────

def chart_by_region(df: pd.DataFrame) -> go.Figure:
    """
    Barras horizontales apiladas: region vs fatalidades por ciudadania.

    Parameters
    ----------
    df : pd.DataFrame
        Columnas requeridas: event_location_region, citizenship.

    Returns
    -------
    go.Figure

    Hints
    -----
    - Agrupa, calcula total por region, ordena descendente.
    - px.bar(orientation="h", barmode="stack", color="citizenship",
             color_discrete_map=PALETTE)
    - Titulo: "Fatalidades por Region"
    """
    # TODO: implementar
    raise NotImplementedError("chart_by_region pendiente")


# ── Grafico 6 ─────────────────────────────────────────────────────────────────

def chart_top_locations(df: pd.DataFrame) -> go.Figure:
    """
    Treemap jerarquico: Region -> Distrito -> Localizacion.

    Parameters
    ----------
    df : pd.DataFrame
        Columnas: event_location_region, event_location_district, event_location.

    Returns
    -------
    go.Figure

    Hints
    -----
    - px.treemap(path=[px.Constant("Total"), "event_location_region",
                       "event_location_district", "event_location"])
    - color_continuous_scale="Reds"
    - Titulo: "Distribucion Geografica"
    """
    # TODO: implementar
    raise NotImplementedError("chart_top_locations pendiente")


# ── Grafico 7 (reto) ──────────────────────────────────────────────────────────

def chart_killed_by(df: pd.DataFrame) -> go.Figure:
    """
    Dona: proporcion de fatalidades por "killed_by".

    Parameters
    ----------
    df : pd.DataFrame
        Columna requerida: killed_by.

    Returns
    -------
    go.Figure

    Hints
    -----
    - df["killed_by"].value_counts() para los datos.
    - px.pie(hole=0.45)
    - Titulo: "Quien causo las fatalidades"
    - Reto: anadir un segundo grafico px.bar con evolucion temporal de killed_by
    """
    # TODO: implementar (reto Dia 3)
    raise NotImplementedError("chart_killed_by pendiente")
