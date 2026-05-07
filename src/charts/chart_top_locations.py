# src/charts/chart_top_locations.py

import pandas as pd
import plotly.express as px


from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered

def chart_top_locations(df: pd.DataFrame):
    """Treemap jerarquico: Region -> Distrito -> Localizacion."""
    df_plot = df.dropna(subset=["event_location_region"])
    
    total = len(df_plot)
    title = f"Distribución Geográfica ({total:,} registros)"
    
    region_colors = {
    "West Bank": "#000080",
    "Gaza Strip": "#FC0000",
    "Israel": "#40E0D0"
}
    
    fig = px.treemap(
        df_plot,
        path=[
            px.Constant("Total"),
            "event_location_region",
            "event_location_district",
            "event_location"
        ],
        title=title,
        color="event_location_region",
        color_discrete_map=region_colors,
        branchvalues="total",
    )
    
    fig.update_traces(
        textinfo="label+value+percent entry",
        hovertemplate="<b>%{label}</b><br>Registros: %{value}<br>%{percentRoot:.1%}<extra></extra>"
    )
    
    fig.update_layout(
        font=dict(size=18),
        title_font=dict(size=22, color="#333"),
        margin=dict(t=60, l=10, r=10, b=10)
    )
    
    chart_log = get_chart_logger("Grafico_6_TopLocations")
    log = get_chart_logger("charts")
    log_chart_rendered(chart_log, "chart_top_locations", len(df), 100)
    log_chart_rendered(log, "chart_top_locations", len(df), 100)
    
    return fig