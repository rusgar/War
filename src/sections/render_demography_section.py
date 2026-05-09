import streamlit as st

from src.charts.chart_age_distribution import chart_age_distribution
from src.charts.chart_gender_breakdown import chart_gender_breakdown

datos = st.session_state.df_filtrado

def render_demography_section(df_filtrado):
    st.subheader("👥 Demografía")
    col3, col4 = st.columns(2)

    with col3:
        try:
            st.plotly_chart(chart_age_distribution(df_filtrado), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_age_distribution pendiente")

    with col4:
        try:
            st.plotly_chart(chart_gender_breakdown(df_filtrado), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_gender_breakdown pendiente")


render_demography_section(datos)