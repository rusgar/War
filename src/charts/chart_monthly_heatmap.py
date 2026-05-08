# src/charts/chart_monthly_heatmap.py

import pandas as pd
import plotly.graph_objects as go

from src.charts.constants import MONTHS_ES
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered
# Aquí traes la FUNCIÓN que está dentro del archivo

def chart_monthly_heatmap(df: pd.DataFrame) -> "go.Figure":
    """Heatmap: eje X = mes (1-12), eje Y = anio, color = fatalidades."""
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
    
    chart_log = get_chart_logger("Grafico_2_MonthlyHeatmap")
    log = get_chart_logger("charts")
    log_chart_rendered(chart_log, "chart_monthly_heatmap", len(df), 100)
    log_chart_rendered(log, "chart_monthly_heatmap", len(df), 100)
    
    return fig
