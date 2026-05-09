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

    # Combinar con datos adicionales si existen
    df_combined = combine_data(df_original)

    if len(df_combined) > len(df_original):
        st.info(f"📊 Datos combinados: {len(df_combined)} registros (originales: {len(df_original)})")


    # Sidebar y filtros - pasar datos combinados para reflejar cambios
    filters = render_sidebar(df_combined)
    df = apply_filters(df_combined, filters)

    #Cabecera
    render_header_section()

    # KPIs
    try:
        render_kpis(df, df_original)
    except NotImplementedError:
        st.info("⚙️ feature/ui: render_kpis pendiente")
    st.markdown("---")

    #Temporal
    render_temporal_section(df)

    #Demografía
    render_demography_section(df)

    #Geografía
    render_geography_section(df)

    #Killed by
    render_killed_by_section(df)

    #Renderizar gráfico 3D
    render_chart_scatter_3d(df)

    #Estadísticas y exportación
    render_stats_section(df)

    #Tabla de datos
    render_filtered_data_section(df, df_original)

if __name__ == "__main__":
    main()

