# # src/charts/chart_scatter_3d.py

# import pandas as pd
# import plotly.express as px

# from src.charts.constants import PALETTE, MONTHS_ES
# from src.logger.get_chart_logger import get_chart_logger
# from src.logger.log_chart_rendered import log_chart_rendered
# # Aquí traes la FUNCIÓN que está dentro del archivo

# def chart_scatter_3d(df: pd.DataFrame):
#     """Scatter 3D: año vs mes vs edad, coloreado por ciudadanía."""
#     if "date_of_event" in df.columns:
#         df_plot = df.copy()
#         df_plot["date_of_event"] = pd.to_datetime(
#             df_plot["date_of_event"], errors="coerce"
#         )
#     elif "date_of_death" in df.columns:
#         df_plot = df.copy()
#         df_plot["date_of_event"] = pd.to_datetime(
#             df_plot["date_of_death"], errors="coerce"
#         )
#     else:
#         raise KeyError("date_of_event no encontrada y no se puede derivar year/month")

#     df_plot["year"] = df_plot["date_of_event"].dt.year
#     df_plot["month"] = df_plot["date_of_event"].dt.month

#     if "age" not in df_plot.columns:
#         raise KeyError("age column not found")
#     df_plot = df_plot[df_plot["age"].between(0, 110)].copy()

#     if len(df_plot) > 2000:
#         df_plot = df_plot.sample(n=2000, random_state=42)

#     df_plot["year"] = df_plot["year"].astype("Int64").fillna(-1).astype(int)
#     df_plot["month"] = df_plot["month"].astype("Int64").fillna(-1).astype(int)

#     fig = px.scatter_3d(
#         df_plot,
#         x="year",
#         y="month",
#         z="age",
#         color="citizenship",
#         color_discrete_map=PALETTE,
#         symbol="gender",
#         title="Visualización 3D: Año / Mes / Edad",
#         labels={"year": "Año", "month": "Mes", "age": "Edad"},
#         hover_data=["event_location_region"],
#     )

#     fig.update_layout(
#         scene=dict(
#             xaxis=dict(title="Año", tickmode="linear", tick0=2000, dtick=2),
#             yaxis=dict(
#                 title="Mes",
#                 tickmode="array",
#                 tickvals=list(range(1, 13)),
#                 ticktext=MONTHS_ES,
#             ),
#             zaxis=dict(title="Edad"),
#         ),
#         legend=dict(title="Ciudadanía"),
#         height=800,
#     )

#     fig.update_traces(marker=dict(size=3, opacity=0.7))

#     log = get_chart_logger("charts")
#     log_chart_rendered(log, "chart_scatter_3d", len(df_plot))

#     return fig


# src/charts/chart_scatter_3d.py

import pandas as pd
import plotly.express as px

from src.charts.constants import MONTHS_ES

def chart_scatter_3d(df: pd.DataFrame):
    # 1. Preparación de datos (Igual que antes)
    if "date_of_event" in df.columns:
        df_plot = df.copy()
        df_plot["date_of_event"] = pd.to_datetime(df_plot["date_of_event"], errors="coerce")
    elif "date_of_death" in df.columns:
        df_plot = df.copy()
        df_plot["date_of_event"] = pd.to_datetime(df_plot["date_of_death"], errors="coerce")
    else:
        raise KeyError("No se encontró columna de fecha.")

    df_plot["year"] = df_plot["date_of_event"].dt.year
    df_plot["month"] = df_plot["date_of_event"].dt.month
    df_plot = df_plot[df_plot["age"].between(0, 110)].copy()

    # --- CORRECCIÓN CRÍTICA: MUESTREO PROTEGIDO ---
    # En lugar de un sample aleatorio de todo el DF, vamos a proteger a American y Jordanian
    # para que no desaparezcan si son pocos registros.
    
    # target_citizens = ["American", "Jordanian", "Israeli", "Palestinian"]
    
    # Separamos los grupos
    minoritarios = df_plot[df_plot["citizenship"].isin(["American", "Jordanian"])]
    mayoritarios = df_plot[df_plot["citizenship"].isin(["Israeli", "Palestinian"])]
    
    # De los mayoritarios tomamos una muestra, de los minoritarios tomamos TODO
    if len(mayoritarios) > 1500:
        mayoritarios = mayoritarios.sample(n=1500, random_state=42)
    
    # Juntamos de nuevo
    df_plot = pd.concat([mayoritarios, minoritarios])
    # ----------------------------------------------

    df_plot["year"] = df_plot["year"].astype("Int64").fillna(-1).astype(int)
    df_plot["month"] = df_plot["month"].astype("Int64").fillna(-1).astype(int)

    HIGH_CONTRAST_PALETTE = {
        "Palestinian": "#2ECC71",
        "Israeli": "#E74C3C",
        "American": "#3498DB",
        "Jordanian": "#F1C40F"
    }

    fig = px.scatter_3d(
        df_plot,
        x="year",
        y="month",
        z="age",
        color="citizenship",
        color_discrete_map=HIGH_CONTRAST_PALETTE,
        # Forzamos el orden de la leyenda para que siempre aparezcan los 4 nombres
        category_orders={"citizenship": ["Palestinian", "Israeli", "American", "Jordanian"]},
        title="<b>ANÁLISIS ESPACIAL: AÑO / MES / EDAD</b><br><sup>Visualización completa de todas las ciudadanías</sup>",
        labels={"year": "AÑO", "month": "MES", "age": "EDAD", "citizenship": "CIUDADANÍA"}
    )

    fig.update_traces(
        marker=dict(
            size=6, 
            opacity=1.0, 
            line=dict(width=1.5, color="black")
        )
    )

    fig.update_layout(
        width=1300,
        height=900,
        margin=dict(l=0, r=0, b=0, t=100), # Ajustamos márgenes para que el cubo sea más grande
        scene=dict(
            xaxis=dict(title="AÑO", tickfont=dict(color="black", family="Arial Black")),
            yaxis=dict(title="MES", ticktext=MONTHS_ES, tickvals=list(range(1,13)), tickfont=dict(color="black", family="Arial Black")),
            zaxis=dict(title="EDAD", tickfont=dict(color="black", family="Arial Black")),
        ),
        legend=dict(
            title=dict(text="CIUDADANÍA"),
            font=dict(size=14, family="Arial Black", color="black"),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            # Aseguramos que la leyenda sea visible y no se corte
            itemsizing='constant'
        )
    )

    return fig