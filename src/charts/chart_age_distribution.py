# src/charts/chart_age_distribution.py

import pandas as pd
import plotly.express as px

from src.charts.constants import PALETTE
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered
# Aquí traes la FUNCIÓN que está dentro del archivo


def chart_age_distribution(df: pd.DataFrame) -> "go.Figure":
    """Histograma de edades con marginal rug, por ciudadania."""
    log = get_chart_logger("chart_age_distribution")

    df_plot = df[df["age"].between(0, 110)].copy()
    df_plot["age"] = pd.to_numeric(df_plot["age"], errors="coerce")
    df_plot = df_plot.dropna(subset=["age", "citizenship"])
    df_plot["citizenship"] = df_plot["citizenship"].astype(str)

    fig = px.histogram(
        df_plot,
        x="age",
        nbins=40,
        marginal="rug",
        color="citizenship",
        color_discrete_map=PALETTE,
        opacity=0.7,
    )

    if not df_plot.empty and not df_plot["age"].isna().all():
        media = df_plot["age"].mean()
        fig.add_vline(x=media, line_dash="dash", line_color="gray")

    fig.update_layout(title="Distribucion de Edades")

   
    log_chart_rendered(log, "chart_age_distribution", len(df_plot))

    return fig