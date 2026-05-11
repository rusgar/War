import streamlit as st

from src.charts.chart_killed_by import chart_killed_by


def render_killed_by_section(df_filtrado):
    st.subheader("⚠️ Causa de la fatalidad")

    try:
        st.plotly_chart(chart_killed_by(df_filtrado), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_killed_by pendiente (Día 3)")

