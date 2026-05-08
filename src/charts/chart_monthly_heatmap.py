# # src/charts/chart_monthly_heatmap.py

# import pandas as pd
# import plotly.graph_objects as go

# from src.charts.constants import MONTHS_ES
# from src.logger.get_chart_logger import get_chart_logger
# from src.logger.log_chart_rendered import log_chart_rendered
# # Aquí traes la FUNCIÓN que está dentro del archivo

# def chart_monthly_heatmap(df: pd.DataFrame) -> "go.Figure":
#     """Heatmap: eje X = mes (1-12), eje Y = anio, color = fatalidades."""
#     pivot = df.groupby(["year", "month"]).size().unstack(fill_value=0)
    
#     fig = go.Figure(data=go.Heatmap(
#         z=pivot.values,
#         x=MONTHS_ES,
#         y=pivot.index,
#         colorscale=[[0, "#ADAD91"], [0.25, "#0053EC"], [0.5, "#04FF04"], [1, "#FF0000"]],
#         hovertemplate="Año: %{y}<br>Mes: %{x}<br>Fatalidades: %{z}<extra></extra>"
#     ))
    
#     fig.update_layout(
#         title="Fatalidades por Mes y Año",
#         xaxis_title="Mes",
#         yaxis_title="Año",
#         yaxis=dict(autorange="reversed")
#     )
    
#     chart_log = get_chart_logger("Grafico_2_MonthlyHeatmap")
#     log = get_chart_logger("charts")
#     log_chart_rendered(chart_log, "chart_monthly_heatmap", len(df), 100)
#     log_chart_rendered(log, "chart_monthly_heatmap", len(df), 100)
    
#     return fig



# # src/charts/chart_monthly_heatmap.py

# import pandas as pd
# import plotly.graph_objects as go

# from src.charts.constants import MONTHS_ES
# from src.logger.get_chart_logger import get_chart_logger
# from src.logger.log_chart_rendered import log_chart_rendered

# def chart_monthly_heatmap(df: pd.DataFrame) -> "go.Figure":
#     """
#     Heatmap Gigante: Maximizando visibilidad, tamaño de rejilla y tipografía.
#     """
#     # 1. Preparación de datos (asegurando el orden de los meses)
#     pivot = df.groupby(["year", "month"]).size().unstack(fill_value=0)
#     pivot = pivot.reindex(columns=range(1, 13), fill_value=0)

#     # 2. Configuración de la traza del Heatmap
#     fig = go.Figure(data=go.Heatmap(
#         z=pivot.values,
#         x=MONTHS_ES,
#         y=pivot.index,
#         # 'xgap' y 'ygap' crean las "calles" blancas entre celdas para mayor claridad
#         xgap=10, 
#         ygap=10,
#         colorscale=[[0, "#ADAD91"], [0.25, "#0053EC"], [0.5, "#04FF04"], [1, "#FF0000"]],
#         hovertemplate="Año: %{y}<br>Mes: %{x}<br>Fatalidades: %{z}<extra></extra>",
#         # Texto dentro de las celdas
#         text=pivot.values,
#         texttemplate="%{text}",
#         # Fuente masiva y legible
#         textfont={
#             "size": 16, 
#             "family": "Arial Black", 
#             "color": "Black"
#         }
#     ))
    
#     # 3. Diseño del Layout (Formato Grande y Amplio)
#     fig.update_layout(
#         title=dict(
#             text="FATALIDADES POR MES Y AÑO",
#             font=dict(size=32, family="Arial Black"),
#             x=0.5,
#             y=0.95
#         ),
#         xaxis=dict(
#             title=dict(text="MESES", font=dict(size=20)),
#             tickfont=dict(size=18, family="Arial Black"),
#             side="top" # Meses arriba para no forzar la vista abajo
#         ),
#         yaxis=dict(
#             title=dict(text="AÑOS", font=dict(size=20)),
#             autorange="reversed", 
#             dtick=1,
#             tickfont=dict(size=18, family="Arial Black")
#         ),
#         # Dimensiones del lienzo (puedes subirlas más si es necesario)
#         width=1200,  # Muy ancho para separar los meses
#         height=800,   # Muy alto para dar aire a los años
#         margin=dict(l=150, r=150, t=180, b=100),
#         paper_bgcolor="white",
#         plot_bgcolor="rgba(0,0,0,0)" # Fondo limpio
#     )
    
#     # 4. Logs
#     chart_log = get_chart_logger("Grafico_2_MonthlyHeatmap")
#     log = get_chart_logger("charts")
#     log_chart_rendered(chart_log, "chart_monthly_heatmap", len(df), 100)
#     log_chart_rendered(log, "chart_monthly_heatmap", len(df), 100)
    
#     return fig


# src/charts/chart_monthly_heatmap.py

import pandas as pd
import plotly.graph_objects as go

from src.charts.constants import MONTHS_ES
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered

def chart_monthly_heatmap(df: pd.DataFrame) -> "go.Figure":
    """
    Heatmap Gigante: Con colores de ejes personalizables.
    """
    # 1. Preparación de datos
    pivot = df.groupby(["year", "month"]).size().unstack(fill_value=0)
    pivot = pivot.reindex(columns=range(1, 13), fill_value=0)

    # --- DEFINE AQUÍ TU COLOR FAVORITO ---
    MI_COLOR_FAVORITO = "#2C3E50"  # Puedes usar 'black', 'blue', '#HEX', etc.
    # -------------------------------------

    # 2. Configuración del Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=MONTHS_ES,
        y=pivot.index,
        xgap=10, 
        ygap=10,
        colorscale=[[0, "#ADAD91"], [0.25, "#0053EC"], [0.5, "#04FF04"], [1, "#FF0000"]],
        hovertemplate="Año: %{y}<br>Mes: %{x}<br>Fatalidades: %{z}<extra></extra>",
        text=pivot.values,
        texttemplate="%{text}",
        textfont={
            "size": 16,  
            "family": "Arial Black",
            "color": "Black" # El número de adentro suele ir en blanco por el contraste
        }
    ))
    
    # 3. Diseño del Layout
    fig.update_layout(
        title=dict(
            text="FATALIDADES POR MES Y AÑO",
            font=dict(size=32, family="Arial Black", color="White"), # Color del título
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title=dict(text="MESES", font=dict(size=20, family="Arial Black", color="White")),
            # CAMBIO DE COLOR EN MESES
            tickfont=dict(size=18, family="Arial Black", color="White"), 
            side="top"
        ),
        yaxis=dict(
            title=dict(text="AÑOS", font=dict(size=20, family="Arial Black", color="White")),
            autorange="reversed", 
            dtick=1,
            # CAMBIO DE COLOR EN AÑOS
            tickfont=dict(size=18, family="Arial Black", color="White")
        ),
        width=1400,
        height=900,
        margin=dict(l=150, r=150, t=180, b=100),
        paper_bgcolor="black",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    # 4. Logs
    chart_log = get_chart_logger("Grafico_2_MonthlyHeatmap")
    log = get_chart_logger("charts")
    log_chart_rendered(chart_log, "chart_monthly_heatmap", len(df), 100)
    log_chart_rendered(log, "chart_monthly_heatmap", len(df), 100)
    
    return fig