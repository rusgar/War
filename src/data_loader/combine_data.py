import streamlit as st
import pandas as pd
from src.logger.setup_logger import setup_logger

# Logger principal de la app
log = setup_logger("dashboard")


def combine_data(original_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combina datos originales con datos adicionales cargados por el usuario.
    
    Parameters
    ----------
    original_df : pd.DataFrame
        DataFrame original cargado desde el archivo principal
        
    Returns
    -------
    pd.DataFrame
        DataFrame combinado
    """
    from src.data_loader._normalize_columns import _normalize_columns
    from src.data_loader._apply_type_conversions import _apply_type_conversions
    from src.data_loader._add_derived_features import _add_derived_features
    
    combined = original_df.copy()
    
    # Verificar si hay datos adicionales en session_state
    if "additional_data" in st.session_state:
        additional_dfs = st.session_state.additional_data
        
        for df_add in additional_dfs:
            # Hacer una copia para no modificar el original
            df_add = df_add.copy()
            
            # Asegurar que el DataFrame adicional tenga las mismas columnas
            # Rellenar columnas faltantes con None
            for col in combined.columns:
                if col not in df_add.columns:
                    df_add[col] = None
            
            # Reordenar columnas para que coincidan
            df_add = df_add[combined.columns]
            
            # Concatenar
            combined = pd.concat([combined, df_add], ignore_index=True)
        
        # Reaplicar procesamiento si es necesario
        # (solo si las columnas numericas/fechas necesitan conversion)
        try:
            combined = (combined.pipe(_normalize_columns)
                             .pipe(_apply_type_conversions)
                             .pipe(_add_derived_features))
        except Exception as e:
            log.warning("Error al reprocesar datos combinados: %s", str(e))
    
    return combined

