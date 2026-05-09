# # src/charts/chart_gender_breakdown.py

# import pandas as pd
# import plotly.express as px

# from src.charts.constants import PALETTE
# from src.logger.get_chart_logger import get_chart_logger
# from src.logger.log_chart_rendered import log_chart_rendered
# # Aquí traes la FUNCIÓN que está dentro del archivo

# def chart_gender_breakdown(df: pd.DataFrame):
#     """Sunburst de dos niveles: ciudadania -> genero."""
#     df_plot = df.copy()
#     df_plot = df_plot.dropna(subset=["gender"])
    
#     total = len(df_plot)
#     title = f"Distribución por Ciudadanía y Género ({total:,} registros)"
    
#     fig = px.sunburst(
#         df_plot,
#         path=["citizenship", "gender"],
#         title=title,
#         color="citizenship",
#         color_discrete_map=PALETTE,
#         hover_data={"gender": True, "citizenship": False},
#     )
    
#     fig.update_traces(
#         textinfo="label+percent entry",
#         textfont=dict(size=24, color="black"),
#         marker=dict(line=dict(color="white", width=2)),
#         hovertemplate="<b>%{label}</b><br>Registros: %{value}<br>Porcentaje: %{percentEntry}<extra></extra>"
#     )
    
#     fig.update_layout(
#         font=dict(size=16),
#         title_font=dict(size=20, color="#333"),
#         margin=dict(t=80, l=20, r=20, b=20),
#         width=600,
#         height=600,
#         legend=dict(
#             title="Ciudadanía",
#             orientation="h",
#             yanchor="bottom",
#             y=-0.1,
#             xanchor="center",
#             x=0.5
#         )
#     )
    
#     chart_log = get_chart_logger("Grafico_4_GenderBreakdown")
#     log = get_chart_logger("charts")
#     log_chart_rendered(chart_log, "chart_gender_breakdown", len(df), 100)
#     log_chart_rendered(log, "chart_gender_breakdown", len(df), 100)
    
#     return fig

# src/charts/chart_gender_breakdown.py

import pandas as pd
import plotly.express as px

from src.charts.constants import PALETTE
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered

def chart_gender_breakdown(df: pd.DataFrame):
    """Sunburst de dos niveles: ciudadania -> genero."""
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
        # Eliminamos hover_data redundante para limpiar el hover
    )
    
    fig.update_traces(
        textinfo="label+percent entry",
        # Texto dentro de las porciones del gráfico
        textfont=dict(size=18, family="Arial Black", color="Black"), 
        marker=dict(line=dict(color="white", width=2)),
        hovertemplate="<b>%{label}</b><br>Registros: %{value}<br>Porcentaje: %{percentEntry}<extra></extra>"
    )
    
    fig.update_layout(
        # COLOR DEL TÍTULO EN BLANCO
        title=dict(
            text=title,
            font=dict(size=24, family="Arial Black", color="white"),
            x=0.5,
            xanchor="center"
        ),
        # Fondo oscuro opcional o transparente para que el blanco resalte 
        # (Si el fondo de tu app es oscuro, se verá perfecto)
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        
        margin=dict(t=100, l=20, r=20, b=20),
        width=800,  # Aumentado para mejor visibilidad
        height=800, # Aumentado
        
        legend=dict(
            title=dict(text="Ciudadanía", font=dict(color="white")),
            font=dict(color="white"),
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        )
    )
    
    chart_log = get_chart_logger("Grafico_4_GenderBreakdown")
    log = get_chart_logger("charts")
    log_chart_rendered(chart_log, "chart_gender_breakdown", len(df), 100)
    log_chart_rendered(log, "chart_gender_breakdown", len(df), 100)
    
    return fig