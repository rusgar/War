"""
app.py
======
Punto de entrada del dashboard.

ESTADO: Proporcionado por el profesor como esqueleto de integracion.
        La rama feature/ui puede modificar el layout y la estructura.
        No modificar las importaciones sin consenso del equipo.

Ejecutar: streamlit run app.py
"""

import streamlit as st

# Estas importaciones asumen que habeis creado la carpeta src/
# Adaptad la ruta si vuestra estructura es diferente
from src.data_loader.load_data import load_data
from src.data_loader.combine_data import combine_data

from src.logger.setup_logger import setup_logger
from src.filters.render_sidebar import render_sidebar
from src.filters.apply_filters import  apply_filters
from src.kpis.render_kpis import render_kpis


from src.sections.render_filtered_data_section import render_filtered_data_section
from src.sections.render_header_section import render_header_section
from src.sections.render_temporal_section import render_temporal_section
from src.sections.render_demography_section import render_demography_section
from src.sections.render_geography_section import render_geography_section
from src.sections.render_killed_by_section import render_killed_by_section
from src.sections.render_chart_geospatial import render_chart_geospatial
from src.sections.render_stats_section import render_stats_section
from src.sections.render_chart_scatter_3d import render_chart_scatter_3d

# ── Configuracion ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Conflict Fatalities Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Logger principal de la app
log = setup_logger("dashboard")


# ── Datos (cacheados) ─────────────────────────────────────────────────────────

@st.cache_data
def get_data():
    df = load_data()
    log.info("Datos cargados en cache: %d filas", len(df))
    return df


# ── App ───────────────────────────────────────────────────────────────────────

def main():

    df_original = get_data()
    st.session_state.df_original = df_original
    st.session_state.df_publico = combine_data(df_original)

    # Sidebar y filtros - pasar datos combinados para reflejar cambios
    filters = render_sidebar(st.session_state.df_publico)
    df_filtrado = apply_filters(st.session_state.df_publico, filters)

    st.session_state.df_filtrado = df_filtrado

    if len(st.session_state.df_publico) > len(st.session_state.df_original):
        st.info(f"📊 Datos combinados: {len(st.session_state.df_publico)} registros (originales: {len(st.session_state.df_original)})")

    #Cabecera
    render_header_section()

    # KPIs
    try:
        render_kpis(st.session_state.df_filtrado, st.session_state.df_original)
    except NotImplementedError:
        st.info("⚙️ feature/ui: render_kpis pendiente")
    st.markdown("---")


    st.subheader("📊 Visualizador de Gráficos")

    chart_options = {
        "📅 Evolución temporal + 📊 Heatmap mensual": render_temporal_section,
        "👤 Distribución por edad + 🚻 Desglose por género": render_demography_section,
        "🗺️ Por región + 📍 Top ubicaciones": render_geography_section,
        "⚠️ Causa de fatalidad": render_killed_by_section,
        "🔮 Scatter 3D (año/mes/edad)": render_chart_scatter_3d,
        "🗺️ Mapa geoespacial": render_chart_geospatial,

    }

    selected_chart = st.selectbox("Selecciona una gráfica:", list(chart_options.keys()))

    try:
        chart_func = chart_options[selected_chart]
        
        chart_func(st.session_state.df_filtrado)
        
    except NotImplementedError:
        st.info(f"⚙️ {selected_chart} pendiente")






    # #Temporal
    # render_temporal_section(df_filtrado)

    # #Demografía
    # render_demography_section(df_filtrado)

    # #Geografía
    # render_geography_section(df_filtrado)

    # #Killed by
    # render_killed_by_section(df_filtrado)

    # #Renderizar gráfico 3D
    # render_chart_scatter_3d(df_filtrado)

    # #Gráfico tabla y mapa
    # render_chart_geospatial(df_filtrado)

    #Estadísticas y exportación
    render_stats_section(df_filtrado)

    #Tabla de datos
    render_filtered_data_section(df_filtrado, df_original)

if __name__ == "__main__":
    main()

