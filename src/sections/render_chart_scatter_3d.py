from src.charts.chart_scatter_3d import chart_scatter_3d
import streamlit as st

datos = st.session_state.df_filtrado

def render_chart_scatter_3d(df_filtrado):
    st.subheader("⚠️ Scatter 3D: año vs mes vs edad")
    try:
        st.plotly_chart(chart_scatter_3d(df_filtrado), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_scatter_3d pendiente (Día 4)")

render_chart_scatter_3d(datos)  