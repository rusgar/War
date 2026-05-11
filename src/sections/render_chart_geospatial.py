import streamlit as st

from src.charts.chart_geospatial import render_two


def render_chart_geospatial(df_filtrado):
    st.subheader("⚠️ Scatter 3D: año vs mes vs edad")
    try:
        render_two(df_filtrado)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_scatter_3d pendiente (Día 4)")

