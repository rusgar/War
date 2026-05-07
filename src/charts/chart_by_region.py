# src/charts/chart_by_region.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.charts.constants import PALETTE


def chart_by_region(df: pd.DataFrame) -> "go.Figure":
    """Barras horizontales apiladas: region vs fatalidades por ciudadania."""
    df_counts = (
        df.groupby(["event_location_region", "citizenship"])
        .size()
        .reset_index(name="count")
    )

    region_totals = (
        df_counts.groupby("event_location_region")["count"]
        .sum()
        .sort_values(ascending=True)
        .index
    )

    fig = px.bar(
        df_counts,
        y="event_location_region",
        x="count",
        color="citizenship",
        orientation="h",
        barmode="stack",
        color_discrete_map=PALETTE,
        category_orders={"event_location_region": list(region_totals)},
        labels={
            "event_location_region": "Región",
            "count": "Número de Fatalidades",
            "citizenship": "Ciudadanía"
        },
        title="<b>Fatalidades por Región</b>"
    )

    fig.update_layout(
        xaxis_title="Fatalidades",
        yaxis_title=None,
        legend_title="Ciudadanía",
        hovermode="y unified"
    )

    return fig