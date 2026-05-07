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
    df_original = get_data()

    # Sidebar y filtros
    filters = render_sidebar(df_original)
    df = apply_filters(df_original, filters)

    # Cabecera
    st.title("📊 Conflict Fatalities Dashboard")
    st.caption(
        "Fuente: B'Tselem · Israeli Information Center for Human Rights · 2000–2023"
    )
    st.markdown("---")

    # KPIs
    try:
        render_kpis(df, df_original)
    except NotImplementedError:
        st.info("⚙️ feature/ui: render_kpis pendiente")
    st.markdown("---")

    # ── Seccion 1: Temporal ───────────────────────────────────────────────────
    st.subheader("📅 Evolución Temporal")

    try:
        st.plotly_chart(chart_fatalities_over_time(df), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_fatalities_over_time pendiente")

    try:
        st.plotly_chart(chart_monthly_heatmap(df), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_monthly_heatmap pendiente")

    # ── Seccion 2: Demografía ─────────────────────────────────────────────────
    st.subheader("👥 Demografía")
    col3, col4 = st.columns(2)

    with col3:
        try:
            st.plotly_chart(chart_age_distribution(df), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_age_distribution pendiente")

    with col4:
        try:
            st.plotly_chart(chart_gender_breakdown(df), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_gender_breakdown pendiente")

    # ── Seccion 3: Geografía ──────────────────────────────────────────────────
    st.subheader("🗺️ Distribución Geográfica")
    col5, col6 = st.columns([1, 2])

    with col5:
        try:
            st.plotly_chart(chart_by_region(df), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_by_region pendiente")

    with col6:
        try:
            st.plotly_chart(chart_top_locations(df), use_container_width=True)
        except NotImplementedError:
            st.info("⚙️ feature/visualization: chart_top_locations pendiente")

    # ── Seccion 4: Killed by ──────────────────────────────────────────────────
    st.subheader("⚠️ Causa de la fatalidad")
    try:
        st.plotly_chart(chart_killed_by(df), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_killed_by pendiente (Día 3)")


    # ── Seccion 5: Scatter 3D ──────────────────────────────────────────────────
    st.subheader("⚠️ Scatter 3D: año vs mes vs edad")
    try:
        st.plotly_chart(chart_scatter_3d(df), use_container_width=True)
    except NotImplementedError:
        st.info("⚙️ feature/visualization: chart_scatter_3d pendiente (Día 4)")

    # ── Seccion 6: Estadisticas y exportacion ─────────────────────────────────
    st.subheader("📊 Estadísticas Descriptivas")
    try:
        stats = compute_descriptive_stats(df)
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

    # ── Seccion 7: Tabla de datos ─────────────────────────────────────────────
    st.subheader("🔎 Datos Filtrados")
    st.caption(f"{len(df):,} registros mostrados de {len(df_original):,} totales")

    cols_display = [
        "name", "date_of_event", "age", "gender",
        "citizenship", "event_location_region",
        "type_of_injury", "killed_by",
    ]
    available = [c for c in cols_display if c in df.columns]
    st.dataframe(df[available].reset_index(drop=True), use_container_width=True, height=350)

    # Boton de descarga
    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=df[available].to_csv(index=False).encode("utf-8"),
        file_name="fatalities_filtered.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
