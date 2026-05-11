
import streamlit as st

from src.charts.chart_by_region import chart_by_region
from src.charts.chart_top_locations import chart_top_locations


def render_geography_section(df_filtrado):
    st.subheader("🗺️ Distribución Geográfica")
    col5, col6 = st.columns([1, 2])

    with col5:
        try:
            st.plotly_chart(chart_by_region(df_filtrado), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_by_region pendiente")

    with col6:
        try:
            st.plotly_chart(chart_top_locations(df_filtrado), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_top_locations pendiente")

