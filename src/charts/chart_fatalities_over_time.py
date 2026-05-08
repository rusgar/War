# src/charts/chart_fatalities_over_time.py

import pandas as pd
import plotly.express as px

from src.charts.constants import PALETTE
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered
# Aquí traes la FUNCIÓN que está dentro del archivo

def chart_fatalities_over_time(df: pd.DataFrame):
    """Área apilada: fatalidades por año, segmentado por ciudadanía."""
    grouped = df.groupby(["year", "citizenship"]).size().reset_index(name="total")

    fig = px.area(
        grouped,
        x="year",
        y="total",
        color="citizenship",
        color_discrete_map=PALETTE,
        title="<b>Evolución Temporal de Fatalidades</b><br><sup>Fatalidades por año según ciudadanía</sup>",
        labels={"year": "Año", "total": "Fatalidades", "citizenship": "Ciudadanía"},
        hover_data={"year": True, "total": ":,"},
        groupnorm="",
    )

    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                      "Año: %{x}<br>" +
                      "Fatalidades: %{y:,}<extra></extra>",
        line={"width": 2},
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(
            tickmode="linear",
            dtick=1,
            tickangle=-45,
            showgrid=True,
            gridcolor="rgba(128,128,128,0.2)",
            title_font=dict(size=14),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(128,128,128,0.2)",
            title_font=dict(size=14),
            ticksuffix="",
        ),
        legend=dict(
            title="Ciudadanía",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(128,128,128,0.3)",
            borderwidth=1,
        ),
        title=dict(
            font=dict(size=20, color="#1a1a2e"),
            x=0.5,
            xanchor="center",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=60, r=30, t=80, b=60),
        height=450,
    )

    for citizenship in grouped["citizenship"].unique():
        subset = grouped[grouped["citizenship"] == citizenship]
        max_row = subset.loc[subset["total"].idxmax()]
        fig.add_annotation(
            x=max_row["year"],
            y=max_row["total"],
            text=f"{max_row['total']:,}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor="gray",
            font=dict(size=10, color="#333"),
            bgcolor="rgba(255,255,255,0.9)",
            borderpad=4,
            ay=-30 if max_row["citizenship"] != "Palestinian" else 30,
        )

    chart_log = get_chart_logger("Grafico_1_FatalitiesOverTime")
    log = get_chart_logger("charts")
    log_chart_rendered(chart_log, "chart_fatalities_over_time", len(df), 100)
    log_chart_rendered(log, "chart_fatalities_over_time", len(df), 100)

    return fig