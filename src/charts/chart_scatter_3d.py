# src/charts/chart_scatter_3d.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.charts.constants import PALETTE, MONTHS_ES
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered
# Aquí traes la FUNCIÓN que está dentro del archivo

def chart_scatter_3d(df: pd.DataFrame) -> "go.Figure":
    """Scatter 3D: año vs mes vs edad, coloreado por ciudadanía."""
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

    log = get_chart_logger("charts")
    log_chart_rendered(log, "chart_scatter_3d", len(df_plot))

    return fig