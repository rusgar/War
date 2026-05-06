# src/charts/chart_fatalities_over_time.py

import pandas as pd
import plotly.express as px

from src.charts.constants import PALETTE, get_chart_logger, log_chart_rendered


def chart_fatalities_over_time(df: pd.DataFrame) -> "go.Figure":
    """Lineas: fatalidades por anio, una linea por ciudadania."""
    grouped = df.groupby(["year", "citizenship"]).size().reset_index(name="total")

    fig = px.line(
        grouped,
        x="year",
        y="total",
        color="citizenship",
        color_discrete_map=PALETTE,
        title="Fatalidades por Año"
    )

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

    chart_log = get_chart_logger("Grafico_1_FatalitiesOverTime")
    log = get_chart_logger("charts")
    log_chart_rendered(chart_log, "chart_fatalities_over_time", len(df), 100)
    log_chart_rendered(log, "chart_fatalities_over_time", len(df), 100)

    return fig