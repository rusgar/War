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

from src.charts.chart_fatalities_over_time import chart_fatalities_over_time
from src.charts.chart_age_distribution import chart_age_distribution
from src.charts.chart_by_region import chart_by_region
from src.charts.chart_top_locations import chart_top_locations
from src.charts.chart_killed_by import chart_killed_by
from src.charts.chart_monthly_heatmap import chart_monthly_heatmap
from src.charts.chart_gender_breakdown import chart_gender_breakdown
from src.charts.chart_scatter_3d import chart_scatter_3d
from src.charts.chart_geospatial import render_two
from src.stats.compute_descriptive_stats import compute_descriptive_stats
from src.stats.export_stats_to_json import export_stats_to_json


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

    # df_original = get_data()

    # # Combinar con datos adicionales si existen
    # df_combined = combine_data(df_original)


# Solo cargamos si no existe ya en el estado de la sesión
    # if 'df_publico' not in st.session_state:
    df_original = get_data()
    st.session_state.df_original = df_original
    st.session_state.df_publico = combine_data(df_original)

    # Ahora puedes aplicar filtros sobre el estado
    filters = render_sidebar(st.session_state.df_publico)
    df_filtrado = apply_filters(st.session_state.df_publico, filters)
    
    # Guardamos el filtrado también si quieres que otras funciones lo vean
    st.session_state.df_filtrado = df_filtrado

    if len(st.session_state.df_publico) > len(st.session_state.df_original):
        st.info(f"📊 Datos combinados: {len(st.session_state.df_publico)} registros (originales: {len(st.session_state.df_original)})")

    # Cabecera
   
    st.title("📊 Conflict Fatalities Dashboard")
    st.caption(
        "Fuente: B'Tselem · Israeli Information Center for Human Rights · 2000–2023"
    )
    st.markdown("---")

    # KPIs
    try:
        render_kpis(st.session_state.df_filtrado, st.session_state.df_original)
    except NotImplementedError:
        st.info("⚙️ feature/ui: render_kpis pendiente")
    st.markdown("---")

    # # ── Seccion 1: Temporal ───────────────────────────────────────────────────
    # st.subheader("📅 Evolución Temporal")

    # try:
    #     st.plotly_chart(chart_fatalities_over_time(df_filtrado), use_container_width=True)
    # except NotImplementedError:
    #     st.info("⚙️ feature/visualization: chart_fatalities_over_time pendiente")

    # try:
    #     st.plotly_chart(chart_monthly_heatmap(df_filtrado), use_container_width=True)
    # except NotImplementedError:
    #     st.info("⚙️ feature/visualization: chart_monthly_heatmap pendiente")

    # # ── Seccion 2: Demografía ─────────────────────────────────────────────────
    # st.subheader("👥 Demografía")
    # col3, col4 = st.columns(2)

    # with col3:
    #     try:
    #         st.plotly_chart(chart_age_distribution(df_filtrado), use_container_width=True)
    #     except NotImplementedError:
    #         st.info("⚙️ feature/visualization: chart_age_distribution pendiente")

    # with col4:
    #     try:
    #         st.plotly_chart(chart_gender_breakdown(df_filtrado), use_container_width=True)
    #     except NotImplementedError:
    #         st.info("⚙️ feature/visualization: chart_gender_breakdown pendiente")

    # # ── Seccion 3: Geografía ──────────────────────────────────────────────────
    # st.subheader("🗺️ Distribución Geográfica")
    # col5, col6 = st.columns([1, 2])

    # with col5:
    #     try:
    #         st.plotly_chart(chart_by_region(df_filtrado), use_container_width=True)
    #     except NotImplementedError:
    #         st.info("⚙️ feature/visualization: chart_by_region pendiente")

    # with col6:
    #     try:
    #         st.plotly_chart(chart_top_locations(df_filtrado), use_container_width=True)
    #     except NotImplementedError:
    #         st.info("⚙️ feature/visualization: chart_top_locations pendiente")

    # # ── Seccion 4: Killed by ──────────────────────────────────────────────────
    # st.subheader("⚠️ Causa de la fatalidad")
    # try:
    #     st.plotly_chart(chart_killed_by(df_filtrado), use_container_width=True)
    # except NotImplementedError:
    #     st.info("⚙️ feature/visualization: chart_killed_by pendiente (Día 3)")

    # # ── Seccion 5: Scatter 3D ──────────────────────────────────────────────────
    # st.subheader("⚠️ Scatter 3D: año vs mes vs edad")
    # try:
    #     st.plotly_chart(chart_scatter_3d(df_filtrado), use_container_width=True)
    # except NotImplementedError:
    #     st.info("⚙️ feature/visualization: chart_scatter_3d pendiente (Día 4)")

    # # ── Seccion 6: Estadisticas y exportacion ─────────────────────────────────
    st.subheader("📊 Estadísticas Descriptivas")
    try:
        stats = compute_descriptive_stats(st.session_state.df_filtrado)
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Edad media", f"{stats['age_stats']['mean']:.1f}")
        with col_s2:
            st.metric("Edad mediana", f"{stats['age_stats']['median']:.1f}")
        with col_s3:
            st.metric("% Menores", f"{stats['pct_minors']:.1f}%")

        if st.button("💾 Exportar estadísticas a JSON"):
            path = export_stats_to_json(stats)
            st.success(f"Guardado en: {path}")

    except NotImplementedError:
        st.info("⚙️ feature/pipeline: compute_descriptive_stats pendiente")

    # # ── Seccion 7: Tabla de datos ─────────────────────────────────────────────
    # st.subheader("🔎 Datos Filtrados")
    # st.caption(f"{len(st.session_state.df_original):,} registros mostrados de {len(df_filtrado):,} totales")

    # cols_display = [
    #     "name", "date_of_event", "age", "gender",
    #     "citizenship", "event_location_region",
    #     "type_of_injury", "killed_by",
    # ]
    # available = [c for c in cols_display if c in df_filtrado.columns]
    # st.dataframe(df_filtrado[available].reset_index(drop=True), use_container_width=True, height=350)

    # # Boton de descarga
    # st.download_button(
    #     label="⬇️ Descargar datos filtrados (CSV)",
    #     data=df_filtrado[available].to_csv(index=False).encode("utf-8"),
    #     file_name="fatalities_filtered.csv",
    #     mime="text/csv",
    # )

# ── Seccion 8: Selector de graficos ─────────────────────────────────────
    st.subheader("📊 Visualizador de Gráficos")

    chart_options = {
        "📅 Evolución temporal": chart_fatalities_over_time,
        "📊 Heatmap mensual": chart_monthly_heatmap,
        "👤 Distribución por edad": chart_age_distribution,
        "🚻 Desglose por género": chart_gender_breakdown,
        "🗺️ Por región": chart_by_region,
        "📍 Top ubicaciones": chart_top_locations,
        "⚠️ Causa de fatalidad": chart_killed_by,
        "🔮 Scatter 3D (año/mes/edad)": chart_scatter_3d,
        "🗺️ Mapa geoespacial": render_two,

    }

    selected_chart = st.selectbox("Selecciona una gráfica:", list(chart_options.keys()))

    try:
        chart_func = chart_options[selected_chart]
        
        if selected_chart == "🔮 Geopandas":
            # Llamamos a la función directamente sin st.plotly_chart
            # porque render_two ya usa st.plotly_chart internamente
            chart_func(st.session_state.df_filtrado)
        else:
            # Para las demás que sí devuelven una sola figura
            fig = chart_func(st.session_state.df_filtrado)
            st.plotly_chart(fig, use_container_width=True, key=f"chart_{selected_chart}")
    except NotImplementedError:
        st.info(f"⚙️ {selected_chart} pendiente")

if __name__ == "__main__":
    main()
