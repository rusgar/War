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

from src.logger import log_chart_rendered

log = logging.getLogger(__name__)

# Paleta compartida — colores del heatmap
PALETTE = {
    "Palestinian": "#04FF04",      # Verde (del heatmap)
    "Israeli": "#FC0000",          # Rojo oscuro (del heatmap)
    "Foreign": "#FF009D",          # Rosa (del heatmap)
    "Jordanian": "#0053EC",       # Azul (del heatmap)
    "American": "#FBFF00",        # Rosa (del heatmap)
}

# Colores para gráficos 3D y heatmaps
VIVID_COLORS = ["#FF006E", "#00D4FF", "#3A86FF", "#FB5607", "#FFBE0B"]
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
    # Agrupar los datos por año y ciudadanía, y contar las fatalidades
    grouped = df.groupby(["year", "citizenship"]).size().reset_index(name="total")

    # Crear la figura de líneas
    fig = px.line(
        grouped,
        x="year",
        y="total",
        color="citizenship",
        color_discrete_map=PALETTE,
        title="Fatalidades por Año"
    )

    # Anotar el máximo de cada ciudadanía (opcional)
    for citizenship in grouped["citizenship"].unique():
        subset = grouped[grouped["citizenship"] == citizenship]
        max_row = subset.loc[subset["total"].idxmax()]
        fig.add_annotation(
            x=max_row["year"],
            y=max_row["total"],
            text=f"Máximo: {max_row['total']}",
            showarrow=True,
            arrowhead=2
        )

    # Loguear el renderizado del gráfico
    log_chart_rendered(log, "chart_fatalities_over_time", len(df))

    return fig


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
    pivot = df.groupby(["year", "month"]).size().unstack(fill_value=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=MONTHS_ES,
        y=pivot.index,
        colorscale=[[0, "#ADAD91"], [0.25, "#0053EC"], [0.5, "#04FF04"], [1, "#FF0000"]],
        hovertemplate="Año: %{y}<br>Mes: %{x}<br>Fatalidades: %{z}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Fatalidades por Mes y Año",
        xaxis_title="Mes",
        yaxis_title="Año",
        yaxis=dict(autorange="reversed")
    )
    
    log_chart_rendered(log, "chart_monthly_heatmap", len(df))
    
    return fig


# ── Grafico 2b: Scatter 3D ──────────────────────────────────────────────────────

def chart_scatter_3d(df: pd.DataFrame) -> go.Figure:
    """
    Scatter 3D: año vs mes vs edad, coloreado por ciudadanía.

    Parameters
    ----------
    df : pd.DataFrame
        Columnas requeridas: date_of_event, age, citizenship, gender, event_location_region

    Returns
    -------
    go.Figure

    Hints
    -----
    - Derivar year y month desde date_of_event (o date_of_death si procede)
    - Filtrar age entre 0 y 110
    - Muestrear si hay muchos datos (max 2000 puntos para rendimiento)
    - Usar px.scatter_3d(x="year", y="month", z="age", color="citizenship")
    """
    if "date_of_event" in df.columns:
        df_plot = df.copy()
        df_plot["date_of_event"] = pd.to_datetime(
            df_plot["date_of_event"], errors="coerce"
        )
    elif "date_of_death" in df.columns:
        df_plot = df.copy()
        df_plot["date_of_event"] = pd.to_datetime(
            df_plot["date_of_death"], errors="coerce"
        )
    else:
        raise KeyError("date_of_event no encontrada y no se puede derivar year/month")

    df_plot["year"] = df_plot["date_of_event"].dt.year
    df_plot["month"] = df_plot["date_of_event"].dt.month

    if "age" not in df_plot.columns:
        raise KeyError("age column not found")
    df_plot = df_plot[df_plot["age"].between(0, 110)].copy()

    if len(df_plot) > 2000:
        df_plot = df_plot.sample(n=2000, random_state=42)

    # Asegurar que year y month sean enteros para Plotly
    df_plot["year"] = df_plot["year"].astype("Int64").fillna(-1).astype(int)
    df_plot["month"] = df_plot["month"].astype("Int64").fillna(-1).astype(int)

    fig = px.scatter_3d(
        df_plot,
        x="year",
        y="month",
        z="age",
        color="citizenship",
        color_discrete_map=PALETTE,
        symbol="gender",
        title="Visualización 3D: Año / Mes / Edad",
        labels={"year": "Año", "month": "Mes", "age": "Edad"},
        hover_data=["event_location_region"],
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Año", tickmode="linear", tick0=2000, dtick=2),
            yaxis=dict(
                title="Mes",
                tickmode="array",
                tickvals=list(range(1, 13)),
                ticktext=MONTHS_ES,
            ),
            zaxis=dict(title="Edad"),
        ),
        legend=dict(title="Ciudadanía"),
    )

    fig.update_traces(marker=dict(size=3, opacity=0.7))

    log_chart_rendered(log, "chart_scatter_3d", len(df_plot))

    return fig


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
    df_plot = df.copy()
    df_plot = df_plot.dropna(subset=["gender"])
    
    total = len(df_plot)
    title = f"Distribución por Ciudadanía y Género ({total:,} registros)"
    
    fig = px.sunburst(
        df_plot,
        path=["citizenship", "gender"],
        title=title,
        color="citizenship",
        color_discrete_map=PALETTE,
        hover_data={"gender": True, "citizenship": False},
    )
    
    fig.update_traces(
        textinfo="label+percent entry",
        textfont=dict(size=14, color="white"),
        marker=dict(line=dict(color="white", width=2)),
        hovertemplate="<b>%{label}</b><br>Registros: %{value}<br>Porcentaje: %{percentEntry}<extra></extra>"
    )
    
    fig.update_layout(
        font=dict(size=16),
        title_font=dict(size=20, color="#333"),
        margin=dict(t=80, l=20, r=20, b=20),
        width=600,
        height=600,
        legend=dict(
            title="Ciudadanía",
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        )
    )
    
    log_chart_rendered(log, "chart_gender_breakdown", len(df))
    
    return fig


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
