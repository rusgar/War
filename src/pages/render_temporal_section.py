import streamlit as st

from src.charts.chart_fatalities_over_time import chart_fatalities_over_time
from src.charts.chart_monthly_heatmap import chart_monthly_heatmap


def render_temporal_section(df):
    st.subheader("📅 Evolución Temporal")

    try:
        st.plotly_chart(chart_fatalities_over_time(df), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_fatalities_over_time pendiente")

    try:
        st.plotly_chart(chart_monthly_heatmap(df), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_monthly_heatmap pendiente")
