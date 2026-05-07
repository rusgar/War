import logging

import pandas as pd
import streamlit as st
import random
from pathlib import Path



from src.logger.log_filter_applied import log_filter_applied

log = logging.getLogger(__name__)

def render_sidebar_1(df: pd.DataFrame) -> dict:
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
    
    # --- Rango de Años (Siempre visible por ser el más importante) ---
    st.sidebar.subheader("📅 Temporalidad")
    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    year_range = st.sidebar.slider(
        "Rango de años", 
        min_year, max_year, (min_year, max_year),
        help="Filtra las fatalidades por el año en que ocurrieron."
    )

    st.sidebar.markdown("---")

    # --- Grupos de Filtros Expandibles ---
    with st.sidebar.expander("👤 Perfil de la Víctima", expanded=True):
        citizenship = st.multiselect(
            "Ciudadanía",
            sorted(df["citizenship"].dropna().unique()),
            placeholder="Selecciona países"
        )
        gender = st.multiselect(
            "Género",
            sorted(df["gender"].dropna().unique()),
            placeholder="Selecciona géneros"
        )

    with st.sidebar.expander("📍 Ubicación y Causa", expanded=False):
        region = st.multiselect(
            "Región",
            sorted(df["event_location_region"].dropna().unique()),
            placeholder="Selecciona regiones"
        )
        killed_by = st.multiselect(
            "Causa de muerte / Responsable",
            sorted(df["killed_by"].dropna().unique()),
            placeholder="Selecciona causas"
        )

    # --- Botón de Reset ---
    if st.sidebar.button("Limpiar todos los filtros", use_container_width=True):
        # 1. Borramos todo lo que Streamlit tiene guardado en memoria
        for key in st.session_state.keys():
            del st.session_state[key]
        
        # 2. Ahora sí, reiniciamos la app desde cero
        st.rerun()

    return {
        "year_range": year_range,
        "citizenship": citizenship,
        "gender": gender,
        "region": region,
        "killed_by": killed_by,
    }