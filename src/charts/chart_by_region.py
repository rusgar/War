# # src/charts/chart_by_region.py

# import pandas as pd
# import plotly.express as px

# from src.charts.constants import PALETTE


# def chart_by_region(df: pd.DataFrame):
#     """Barras horizontales apiladas: region vs fatalidades por ciudadania."""
#     df_counts = (
#         df.groupby(["event_location_region", "citizenship"])
#         .size()
#         .reset_index(name="count")
#     )

#     region_totals = (
#         df_counts.groupby("event_location_region")["count"]
#         .sum()
#         .sort_values(ascending=True)
#         .index
#     )

#     fig = px.bar(
#         df_counts,
#         y="event_location_region",
#         x="count",
#         color="citizenship",
#         orientation="h",
#         barmode="stack",
#         color_discrete_map=PALETTE,
#         category_orders={"event_location_region": list(region_totals)},
#         labels={
#             "event_location_region": "Región",
#             "count": "Número de Fatalidades",
#             "citizenship": "Ciudadanía"
#         },
#         title="<b>Fatalidades por Región</b>"
#     )

#     fig.update_layout(
#         xaxis_title="Fatalidades",
#         yaxis_title=None,
#         legend_title="Ciudadanía",
#         hovermode="y unified"
#     )

#     return fig

# src/charts/chart_by_region.py

import pandas as pd
import plotly.express as px

from src.charts.constants import PALETTE

def chart_by_region(df: pd.DataFrame):
    """
    Versión Compacta: Títulos y leyenda cercanos para eliminar espacios en blanco innecesarios.
    """
    
    # 1. Preparación de datos
    df_counts = (
        df.groupby(["event_location_region", "citizenship"])
        .size()
        .reset_index(name="count")
    )

    region_totals_df = df_counts.groupby("event_location_region")["count"].sum().reset_index()
    region_totals_df = region_totals_df.sort_values(by="count", ascending=True) 
    ordered_regions = region_totals_df["event_location_region"].tolist()

    # 2. Creación del gráfico
    fig = px.bar(
        df_counts,
        y="event_location_region",
        x="count",
        color="citizenship",
        orientation="h",
        barmode="stack",
        color_discrete_map=PALETTE,
        category_orders={"event_location_region": ordered_regions},
        title="<b>DISTRIBUCIÓN GEOGRÁFICA DE FATALIDADES</b>",
        labels={
            "event_location_region": "REGIÓN",
            "count": "FATALIDADES",
            "citizenship": "CIUDADANÍA"
        },
    )

    # 3. Anotaciones de Totales
    for i, region in enumerate(ordered_regions):
        total = region_totals_df[region_totals_df["event_location_region"] == region]["count"].values[0]
        fig.add_annotation(
            x=total,
            y=region,
            text=f" <b>{total:,}</b>",
            showarrow=False,
            xanchor="left",
            font=dict(size=14, color="black", family="Arial Black")
        )

    # SUBTÍTULO: Lo acercamos más al título principal (y=1.08)
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1.08, 
        text="Desglose por región y ciudadanía",
        showarrow=False,
        font=dict(size=20, color="#444", family="Arial black"),
        xanchor="center"
    )

    # 4. Ajustes de Layout Compacto
    fig.update_layout(
        width=1200,
        height=750,
        paper_bgcolor="white",
        plot_bgcolor="rgba(0,0,0,0.02)",
        
        # Reducimos el margen superior de 220 a 160 para eliminar el vacío
        margin=dict(l=180, r=120, t=160, b=80),
        
        title=dict(
            font=dict(size=28, family="Arial Black", color="black"),
            x=0.5,
            y=0.96, # Ajustamos posición del título principal
            xanchor="center"
        ),
        
        legend=dict(
            title=dict(text=""),
            font=dict(size=13, family="Arial Black", color="black"),
            orientation="h",
            yanchor="top",
            y=1.02, # Bajamos la leyenda para que esté pegada al gráfico
            xanchor="center",
            x=0.5,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        ),

        xaxis=dict(
            title=dict(text="NÚMERO TOTAL DE FATALIDADES", font=dict(size=16, family="Arial Black"), standoff=15),
            tickfont=dict(size=14, color="black", family="Arial Black"),
            gridcolor="rgba(0,0,0,0.1)",
            showgrid=True
        ),
        
        yaxis=dict(
            title=None,
            tickfont=dict(size=14, color="black", family="Arial Black"),
            automargin=True
        )
    )

    fig.update_traces(
        marker_line_color="white",
        marker_line_width=1,
    )

    return fig