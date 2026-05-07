import logging

import pandas as pd
import streamlit as st
import random
from pathlib import Path



from src.logger.log_filter_applied import log_filter_applied

log = logging.getLogger(__name__)

def render_sidebar(df: pd.DataFrame) -> dict:
    st.sidebar.header("📊 Panel de Control")
    st.sidebar.markdown("Ajusta los parámetros para filtrar los datos.")

     # --- IMAGEN PORTADA ---
    portada_path = Path("src/filters/img/Portada.png")
    
    if portada_path.exists():
        st.sidebar.image(str(portada_path), caption="📸 Portada", use_container_width=True)
        st.sidebar.markdown("---")
    else:
        st.sidebar.warning("⚠️ No se encontró la imagen 'filters/img/Portada.png'")
        st.sidebar.markdown("---")
    
    # 1. Definimos la función de limpieza (Callback)
    def reset_all_filters():
        st.session_state.year_slider = (int(df["year"].min()), int(df["year"].max()))
        st.session_state.citiz_filter = []
        st.session_state.gender_filter = []
        st.session_state.region_filter = []
        st.session_state.cause_filter = []
    
    # --- Temporalidad ---
    st.sidebar.subheader("📅 Temporalidad")
    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    
    year_range = st.sidebar.slider(
        "Rango de años", 
        min_year, max_year, (min_year, max_year),
        key="year_slider"
    )

    st.sidebar.markdown("---")

    # --- Perfil de la Víctima ---
    with st.sidebar.expander("👤 Perfil de la Víctima", expanded=True):
        citizenship = st.multiselect(
            "Ciudadanía",
            sorted(df["citizenship"].dropna().unique()),
            placeholder="Selecciona países",
            key="citiz_filter"
        )
        gender = st.multiselect(
            "Género",
            sorted(df["gender"].dropna().unique()),
            placeholder="Selecciona géneros",
            key="gender_filter"
        )

    # --- Ubicación y Causa ---
    with st.sidebar.expander("📍 Ubicación y Causa", expanded=False):
        region = st.multiselect(
            "Región",
            sorted(df["event_location_region"].dropna().unique()),
            placeholder="Selecciona regiones",
            key="region_filter"
        )
        killed_by = st.multiselect(
            "Causa de muerte / Responsable",
            sorted(df["killed_by"].dropna().unique()),
            placeholder="Selecciona causas",
            key="cause_filter"
        )

    st.sidebar.markdown("---")

    # 2. El botón ahora usa 'on_click'
    st.sidebar.button(
        "Limpiar todos los filtros", 
        use_container_width=True, 
        type="primary",
        on_click=reset_all_filters  # <--- Esto es la clave
    )

    return {
        "year_range": year_range,
        "citizenship": citizenship,
        "gender": gender,
        "region": region,
        "killed_by": killed_by,
    }