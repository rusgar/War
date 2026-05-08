import pandas as pd
import plotly.express as px
import streamlit as st
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from src.charts.constants import PALETTE, VIVID_COLORS
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered

# --- CONFIGURACIÓN DE GEOPY ---
# Inicializamos el geolocalizador (Nominatim usa OpenStreetMap)
geolocator = Nominatim(user_agent="my_humanitarian_tracker_app")
# Limitador de tasa: Máximo 1 petición por segundo para respetar las políticas de uso
geocode_service = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Diccionario inicial (Caché prioritario)
LOCATION_COORDINATES = {
    # Gaza Strip
    'gaza': (31.5000, 34.4667),
    'north gaza': (31.5500, 34.5000),
    'khan yunis': (31.3444, 34.3061),
    'rafah': (31.2800, 34.2500),
    'deir al-balah': (31.4167, 34.3500),
    'gush katif': (31.3400, 34.2900),
    
    # West Bank
    'nablus': (32.2211, 35.2544),
    'jenin': (32.4594, 35.3006),
    'ramallah and al-bira': (31.9000, 35.2000),
    'ramallah': (31.9000, 35.2000),
    'hebron': (31.5345, 35.0986),
    'tulkarm': (32.3114, 35.0289),
    'bethlehem': (31.7056, 35.2028),
    'east jerusalem': (31.7833, 35.2333),
    'al-quds': (31.7833, 35.2333),
    'jerusalem': (31.7833, 35.2333),
    'jericho': (31.8667, 35.4500),
    'qalqiliya': (32.1897, 34.9706),      
    'tubas': (32.3167, 35.3667),         
    'salfit': (32.0833, 35.1833),
    
    # Israel
    'israel': (31.0461, 34.8516),
    'tel aviv': (32.0853, 34.7818),
    'haifa': (32.7940, 34.9896),
    'beersheba': (31.2528, 34.7915),
    
    # Additional regions
    'asqalan': (31.6667, 34.5667),
    'ashkelon': (31.6667, 34.5667),
    'beer al-sabe': (31.2528, 34.7915),
    'khan younis': (31.3444, 34.3061),
    'khan yunus': (31.3444, 34.3061),
}

def normalize_location_name(name) -> str:
    """Normaliza el nombre y garantiza retorno de string para evitar errores de Pylance."""
    if pd.isna(name) or name is None:
        return ""
    return str(name).strip().lower()

@st.cache_data(show_spinner=False)
def get_coordinates(location_name: str):
    """
    Obtiene coordenadas intentando:
    1. Diccionario local (LOCATION_COORDINATES)
    2. Búsqueda automática en línea via Geopy
    """
    if not location_name:
        return None, None
    
    normalized = normalize_location_name(location_name)
    if not normalized:
        return None, None
    
    # 1. Búsqueda en diccionario estático
    if normalized in LOCATION_COORDINATES:
        return LOCATION_COORDINATES[normalized]
    
    for key, coords in LOCATION_COORDINATES.items():
        if key and (key in normalized or normalized in key):
            return coords
    
    # 2. Búsqueda automática Online (si no está en el diccionario)
    try:
        # Añadimos contexto regional para mejorar precisión
        search_query = f"{location_name}, Palestine"
        location = geocode_service(search_query)
        
        if location:
            res = (location.latitude, location.longitude)
            # Guardamos en el diccionario de la sesión
            LOCATION_COORDINATES[normalized] = res
            return res
    except Exception:
        pass

    return None, None

def render_chart_top_locations(df: pd.DataFrame):
    """Renderiza el gráfico de barras horizontales."""
    logger = get_chart_logger()
    if df is None or df.empty:
        return None
    
    df_plot = df.copy()
    try:
        district_candidates = ['district', 'distrito', 'region', 'location', 'area', 
                               'governorate', 'province', 'admin_region', 'city', 
                               'event_location_district']
        
        found_col = next((c for c in district_candidates if c in df_plot.columns), None)
        if not found_col:
            return None

        df_plot[found_col] = df_plot[found_col].fillna('Unknown').astype(str).str.strip()
        df_clean = df_plot[df_plot[found_col] != 'Unknown']

        location_counts = (
            df_clean.groupby(found_col)
            .size()
            .reset_index(name='fatalities')
            .sort_values('fatalities', ascending=False)
            .head(15)
        )

        fig_bar = px.bar(
            location_counts,
            x='fatalities',
            y=found_col,
            orientation='h',
            title=f"Top 15 Locations by Fatalities ({found_col.capitalize()})",
            labels={'fatalities': 'Number of Fatalities', found_col: 'Location'},
            color='fatalities',
            color_continuous_scale=VIVID_COLORS
        )

        fig_bar.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            template="plotly_dark",
            margin=dict(l=100, r=20, t=60, b=40),
            height=500
        )
        return fig_bar
    except Exception as e:
        st.error(f"Error en barras: {e}")
        return None

def render_map_top_locations(df: pd.DataFrame):
    """Renderiza el mapa usando geolocalización automática para datos nuevos."""
    if df is None or df.empty:
        return None

    try:
        district_candidates = ['district', 'distrito', 'region', 'location', 'area', 
                               'governorate', 'province', 'admin_region', 'city', 
                               'event_location_district']
        
        found_col = next((c for c in district_candidates if c in df.columns), None)
        if not found_col:
            return None

        df_clean = df.copy()
        df_clean[found_col] = df_clean[found_col].fillna('Unknown').astype(str).str.strip()
        df_clean = df_clean[df_clean[found_col] != 'Unknown']
        
        location_counts = (
            df_clean.groupby(found_col)
            .size()
            .reset_index(name='fatalities')
            .sort_values('fatalities', ascending=False)
            .head(15)
        )
        
        # Aplicamos la función con Geopy incorporado
        with st.spinner('Geolocalizando nuevas ubicaciones...'):
            coords = location_counts[found_col].apply(get_coordinates)
            location_counts['lat'] = coords.apply(lambda x: x[0])
            location_counts['lon'] = coords.apply(lambda x: x[1])
        
        location_counts = location_counts.dropna(subset=['lat', 'lon'])
        
        if len(location_counts) == 0:
            return None
        
        fig_map = px.scatter_mapbox(
            location_counts,
            lat='lat', lon='lon',
            size='fatalities',
            color='fatalities',
            color_continuous_scale=VIVID_COLORS,
            size_max=50,
            hover_name=found_col,
            zoom=8,
            center={"lat": 31.7, "lon": 35.2},
            title="Mapa de Fatalidades por Ubicación (Automático)"
        )
        
        fig_map.update_layout(
            mapbox_style="carto-positron",
            height=700,
            template="plotly_dark"
        )
        return fig_map
        
    except Exception as e:
        st.error(f"Error en mapa: {e}")
        return None

def render_two(df: pd.DataFrame):
    """
    Esta función es la que debes llamar en tu selectbox. 
    Se encarga de dibujar ambos elementos en la UI de Streamlit.
    """
    if df is None or df.empty:
        st.warning("No hay datos disponibles")
        return
    
    fig_bar = render_chart_top_locations(df)
    if fig_bar:
        st.plotly_chart(fig_bar, use_container_width=True)
    
    fig_map = render_map_top_locations(df)
    if fig_map:
        st.divider()
        st.plotly_chart(fig_map, use_container_width=True)
    elif fig_bar:
        st.info("Mapa no disponible para estas ubicaciones específicas.")

def render_in_streamlit(df: pd.DataFrame):
    """Alias para mantener compatibilidad."""
    render_two(df)

if __name__ == "__main__":
    # Prueba local
    try:
        test_df = pd.read_csv('data/fatalities.csv')
        
        # Probar gráfico de barras
        fig_bar = render_chart_top_locations(test_df)
        if fig_bar:
            fig_bar.show()
        else:
            print("ERROR: No se pudo crear el gráfico de barras")
        
        # Probar mapa
        fig_map = render_map_top_locations(test_df)
        if fig_map:
            fig_map.show()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()