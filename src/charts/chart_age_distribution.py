# # src/charts/chart_age_distribution.py

# import pandas as pd
# import plotly.express as px

# from src.charts.constants import PALETTE
# from src.logger.get_chart_logger import get_chart_logger
# from src.logger.log_chart_rendered import log_chart_rendered
# # Aquí traes la FUNCIÓN que está dentro del archivo


# def chart_age_distribution(df: pd.DataFrame):
#     """Histograma de edades con marginal rug, por ciudadania."""
#     log = get_chart_logger("chart_age_distribution")

#     df_plot = df[df["age"].between(0, 110)].copy()
#     df_plot["age"] = pd.to_numeric(df_plot["age"], errors="coerce")
#     df_plot = df_plot.dropna(subset=["age", "citizenship"])
#     df_plot["citizenship"] = df_plot["citizenship"].astype(str)

#     fig = px.histogram(
#         df_plot,
#         x="age",
#         nbins=40,
#         marginal="rug",
#         color="citizenship",
#         color_discrete_map=PALETTE,
#         opacity=0.7,
#     )

#     if not df_plot.empty and not df_plot["age"].isna().all():
#         media = df_plot["age"].mean()
#         fig.add_vline(x=media, line_dash="dash", line_color="gray")

#     fig.update_layout(title="Distribucion de Edades")

   
#     log_chart_rendered(log, "chart_age_distribution", len(df_plot))

#     return fig


# src/charts/chart_age_distribution.py

import pandas as pd
import plotly.express as px

from src.charts.constants import PALETTE
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered

def chart_age_distribution(df: pd.DataFrame):
    """
    Distribución de Edades Facetada:
    Muestra 4 ciudadanos (American, Israeli, Jordanian, Palestinian)
    en paneles separados para una comparación limpia y profesional.
    """
    # 1. Filtrado y Limpieza
    target_citizenships = ["American", "Israeli", "Jordanian", "Palestinian"]
    
    df_plot = df[df["citizenship"].isin(target_citizenships)].copy()
    df_plot = df_plot[df_plot["age"].between(0, 100)]
    df_plot = df_plot.dropna(subset=["age", "citizenship"])

    # 2. Creación del Histograma Facetado
    fig = px.histogram(
        df_plot,
        x="age",
        color="citizenship",
        facet_row="citizenship", # Crea una fila por cada ciudadanía
        nbins=40,
        color_discrete_map=PALETTE,
        labels={"age": "Edad", "citizenship": "Ciudadanía"},
        title="<b>ANÁLISIS COMPARATIVO DE EDADES POR CIUDADANÍA</b>",
        height=1000, # Más alto para acomodar las 4 filas
        category_orders={"citizenship": target_citizenships} # Orden específico
    )

    # 3. Personalización de Alta Visibilidad
    fig.update_traces(
        marker_line_color="white",
        marker_line_width=1,
        opacity=0.9
    )

    fig.update_layout(
        font=dict(family="Arial Black", color="black"),
        title=dict(font=dict(size=28), x=0.5, y=0.98),
        margin=dict(t=120, l=100, r=50, b=80),
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0.02)",
        showlegend=False # La leyenda sobra porque cada fila tiene su nombre
    )

    # Ajustar fuentes de los ejes y títulos de las facetas (etiquetas a la derecha)
    fig.update_xaxes(
        title_font=dict(size=18, color="black"),
        tickfont=dict(size=14, color="black"),
        gridcolor="rgba(0,0,0,0.1)"
    )
    
    fig.update_yaxes(
        title_text="Frecuencia",
        title_font=dict(size=16, color="black"),
        tickfont=dict(size=12, color="black"),
        gridcolor="rgba(0,0,0,0.1)"
    )

    # Cambiar el texto de las etiquetas laterales (facetas)
    fig.for_each_annotation(lambda a: a.update(
        text=f"<b>{a.text.split('=')[-1].upper()}</b>",
        font=dict(size=16, color="black")
    ))

    # 4. Logs
    chart_log = get_chart_logger("chart_age_distribution")
    log_chart_rendered(chart_log, "facet_age_dist", len(df_plot), 100)
    
    return fig