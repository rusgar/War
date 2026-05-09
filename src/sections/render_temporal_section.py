import streamlit as st

from src.charts.chart_fatalities_over_time import chart_fatalities_over_time
from src.charts.chart_monthly_heatmap import chart_monthly_heatmap

datos = st.session_state.df_filtrado

def render_temporal_section(df_filtrado):
    st.subheader("📅 Evolución Temporal")

    try:
        st.plotly_chart(chart_fatalities_over_time(df_filtrado), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_fatalities_over_time pendiente")

    try:
        st.plotly_chart(chart_monthly_heatmap(df_filtrado), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_monthly_heatmap pendiente")


render_temporal_section(datos)