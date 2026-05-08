import logging
import pandas as pd
import streamlit as st
from pathlib import Path
from src.data_loader.add_csv import _handle_csv_upload

#from src.logger.log_filter_applied import log_filter_applied

log = logging.getLogger(__name__)

def load_css(file_path):
    """Carga un archivo CSS y lo inyecta en Streamlit"""
    with open(file_path, 'r') as f:
        css_content = f.read()
    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

def render_sidebar(df: pd.DataFrame) -> dict:
    # Cargar CSS personalizado
    css_path = Path(__file__).parent / "styles" / "sidebar.css"
    if css_path.exists():
        load_css(css_path)
    
    st.sidebar.header("📊 Panel de Control")
    _handle_csv_upload(df)
    st.sidebar.markdown("Ajusta los parámetros para filtrar los datos.")

    # --- IMAGEN PORTADA ---
    portada_path = Path("src/filters/img/Portada.png")
    
    if portada_path.exists():
        try:
            try:
                st.sidebar.image(str(portada_path), caption="📸 Portada", use_container_width=True)
            except TypeError:
                try:
                    st.sidebar.image(str(portada_path), caption="📸 Portada", use_column_width=True)
                except TypeError:
                    st.sidebar.image(str(portada_path), caption="📸 Portada")
            st.sidebar.markdown("---")
        except Exception as e:
            st.sidebar.error(f"Error al cargar imagen: {str(e)}")
            st.sidebar.markdown("---")
    else:
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

    # Botón de limpieza
    st.sidebar.button(
        "Limpiar todos los filtros", 
        use_container_width=True, 
        type="primary",
        on_click=reset_all_filters
    )

    # --- SECCIÓN DE COLABORADORES ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Equipo de Desarrollo")
    st.sidebar.markdown("*Dashboard Colaborativo*")
    st.sidebar.markdown("---")
    
    
    colaboradores = [
        {
            "nombre": "Edu Rus",
            "github": "rusgar",  # Reemplaza con usuario real
            "rol": "Docente / Team Lead",
            "icono": "👨‍🏫",
            "badge": "leader",
            "contribucion": "Dirección del proyecto y supervisión"
        },
        {
            "nombre": "Carlos",
            "github": "carlosbarrientosarias27-star", 
            "rol": "Feature Pipelines",
            "icono": "🔧",
            "badge": "pipeline",
            "contribucion": "Implementación de pipelines de datos"
        },
        {
            "nombre": "Israel",
            "github": "israelscr-prog", 
            "rol": "Modularización & Testing",
            "icono": "🧪",
            "badge": "pipeline",
            "contribucion": "Estructura modular y pruebas unitarias"
        },
        {
            "nombre": "Ángel",
            "github": "kindred-98",
            "rol": "Visualizaciones & Backend",
            "icono": "📊",
            "badge": "vis",
            "contribucion": "Gráficos interactivos y lógica backend"
        },
        {
            "nombre": "Andrés",
            "github": "zombiradiactivo",  # Reemplaza con usuario real
            "rol": "Unificación & Integración",
            "icono": "🦄",
            "badge": "unify",
            "contribucion": "Integración de componentes y orquestación"
        }
    ]
    
    
    for colab in colaboradores:
        badge_class = f"member-badge role-{colab['badge']}" if colab['badge'] != "leader" else "member-badge role-leader"
        
        st.sidebar.markdown(
            f'<div class="team-container">'
            f'<a href="https://github.com/{colab["github"]}" target="_blank" style="text-decoration: none;">'
            f'<div class="team-member">'
            f'<div class="member-icon">{colab["icono"]}</div>'
            f'<div class="member-info">'
            f'<span class="member-name">{colab["nombre"]}'
            f'<span class="{badge_class}">{colab["rol"]}</span>'
            f'</span>'
            f'<span class="member-role">📌 {colab["contribucion"]}</span>'
            f'</div>'
            f'</div>'
            f'</a>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        '<div style="text-align: center; font-size: 11px; color: #8b949e;">'
        '<p>🚀 Proyecto colaborativo Fundacion Dicampus</p>'
        '<p>© 2026 - Dashboard de Fatalidades</p>'
        '</div>',
        unsafe_allow_html=True
    )

    return {
        "year_range": year_range,
        "citizenship": citizenship,
        "gender": gender,
        "region": region,
        "killed_by": killed_by,
    }