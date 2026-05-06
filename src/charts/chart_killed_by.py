# src/charts/chart_killed_by.py

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.charts.constants import get_chart_logger, log_chart_rendered


def chart_killed_by(df: pd.DataFrame) -> "go.Figure":
    """Donut Chart de fatalidades y Bar Chart de evolución temporal."""
    counts = df["killed_by"].value_counts().reset_index()
    counts.columns = ["causa", "total"]

    df["date_parsed"] = pd.to_datetime(df["date_of_event"], errors="coerce")
    df["year_month"] = df["date_parsed"].dt.to_period("M").astype(str)
    evolution = df.groupby(["year_month", "killed_by"]).size().reset_index(name="counts")

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "domain"}, {"type": "xy"}]],
        subplot_titles=("Distribución Total", "Evolución Temporal")
    )

    fig.add_trace(
        go.Pie(
            labels=counts["causa"],
            values=counts["total"],
            hole=0.45,
            name="Fatalidades",
            textinfo="percent+label",
            textfont=dict(size=16)
        ),
        row=1, col=1
    )

    for killer in df["killed_by"].unique():
        killer_data = evolution[evolution["killed_by"] == killer]
        fig.add_trace(
            go.Bar(
                x=killer_data["year_month"],
                y=killer_data["counts"],
                name=str(killer)
            ),
            row=1, col=2
        )

    fig.update_layout(
        title_text="<b>Quién causó las fatalidades</b>",
        template="plotly_white",
        legend_title="Causa",
        barmode="stack",
        height=600,
        width=1100,
        font=dict(size=14),
        title_font=dict(size=20)
    )

    return fig