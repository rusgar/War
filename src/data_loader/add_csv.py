import logging

import pandas as pd
import streamlit as st

from src.data_loader.column_mapping import (
    find_column_mapping,
    apply_column_mapping,
    get_unmapped_columns,
)


log = logging.getLogger(__name__)


# Variable de sesion para datos adicionales
ADDITIONAL_DATA_KEY = "additional_data"


def _handle_csv_upload(existing_df: pd.DataFrame):
    """
    Maneja la carga de un CSV adicional y el mapeo de columnas.
    Verifica duplicados basandose en nombre y fecha de evento/muerte.
    
    Parameters
    ----------
    existing_df : pd.DataFrame
        DataFrame existente para verificar duplicados
    """
    import difflib
    import re
    
    st.sidebar.markdown("### 📁 Añadir datos CSV")
    
    # Inicializar estado
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    
    uploaded_file = st.sidebar.file_uploader(
        "Subir CSV adicional",
        type=["csv"],
        key="csv_uploader"
    )
    
    if uploaded_file is not None:
        # Generar ID unico para este archivo
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        # Si este archivo ya fue procesado, no hacer nada
        if file_id in st.session_state.processed_files:
            st.sidebar.info("Este archivo ya fue añadido. Para subir otro, quite este archivo.")
            return
        
        # Leer el CSV subido
        try:
            # Resetear el file pointer
            uploaded_file.seek(0)
            
            # Detectar separador (coma o punto y coma)
            sample = uploaded_file.read(1024).decode('utf-8')
            uploaded_file.seek(0)
            
            # Contar comas y punto y comas en la primera línea
            first_line = sample.split('\n')[0]
            comma_count = first_line.count(',')
            semicolon_count = first_line.count(';')
            
            # Usar el separador más probable
            if semicolon_count > comma_count:
                sep = ';'
            else:
                sep = ','
            
            df_new = pd.read_csv(uploaded_file, sep=sep)
            st.sidebar.success(f"CSV cargado: {len(df_new)} filas (separador: '{sep}')")
            
            # Normalizar nombres de columnas (espacios y guiones a underscore)
            df_new.columns = [
                re.sub(r'[_-]+', '_', c.strip().replace(" ", "_").replace("-", "_"))
                for c in df_new.columns
            ]
            
            # Encontrar mapeo automatico
            mapping = find_column_mapping(
                df_new.columns.tolist(),
                existing_df.columns.tolist()
            )
            
            # Identificar columnas no mapeadas
            unmapped = get_unmapped_columns(mapping)
            
            if unmapped:
                st.sidebar.warning(
                    "Algunas columnas no se mapearon automaticamente"
                )
                
                # Permitir mapeo manual
                st.sidebar.markdown("#### Mapeo manual de columnas")
                
                for col in unmapped:
                    # Buscar coincidencias parciales para sugerir
                    options = ["-- No mapear --"] + existing_df.columns.tolist()
                    
                    # Sugerir la mejor coincidencia
                    best_match_idx = 0
                    similarities = [
                        difflib.SequenceMatcher(
                            None, 
                            col.lower().replace("_", ""), 
                            c.lower().replace("_", "")
                        ).ratio()
                        for c in existing_df.columns.tolist()
                    ]
                    if similarities:
                        max_sim = max(similarities)
                        if max_sim > 0.4:
                            best_match_idx = similarities.index(max_sim) + 1
                    
                    selected = st.sidebar.selectbox(
                        f"Mapear '{col}' a:",
                        options=options,
                        index=best_match_idx,
                        key=f"map_{col}"
                    )
                    
                    if selected != "-- No mapear --":
                        mapping[col] = selected
                    else:
                        mapping[col] = None
            
            # Mostrar mapeo final
            with st.sidebar.expander("Ver mapeo de columnas"):
                for src, tgt in mapping.items():
                    status = "✅" if tgt else "❌"
                    st.text(f"{status} {src} -> {tgt or 'No mapeado'}")
            
            # Aplicar mapeo para verificar duplicados
            df_mapped = apply_column_mapping(df_new, mapping)
            
            # Obtener todos los datos existentes para verificar duplicados
            # Combinar datos originales con datos adicionales previamente añadidos
            existing_for_check = existing_df.copy()
            if ADDITIONAL_DATA_KEY in st.session_state and st.session_state[ADDITIONAL_DATA_KEY]:
                for df_add in st.session_state[ADDITIONAL_DATA_KEY]:
                    existing_for_check = pd.concat([existing_for_check, df_add], ignore_index=True)
            
            # Verificar duplicados
            has_name_col = 'name' in existing_for_check.columns and 'name' in df_mapped.columns
            if not df_mapped.empty and has_name_col:
                duplicate_cols = ['name']
                date_cols = ['date_of_event', 'date_of_death']
                check_cols = duplicate_cols + [c for c in date_cols if c in df_mapped.columns]

                # Función interna para normalizar strings y fechas
                def normalize_series(series, is_date=False):
                    if is_date:
                        # Forzamos formato día/mes/año que es el de tu CSV
                        return pd.to_datetime(series, dayfirst=True, errors='coerce')
                    return series.astype(str).str.strip().str.lower()

                # Preparamos copias limpias para comparar
                df_existing_check = pd.DataFrame()
                df_new_check = pd.DataFrame()

                df_existing_check['name'] = normalize_series(existing_for_check['name'])
                df_new_check['name'] = normalize_series(df_mapped['name'])

                for col in date_cols:
                    if col in existing_for_check.columns and col in df_mapped.columns:
                        df_existing_check[col] = normalize_series(existing_for_check[col], is_date=True)
                        df_new_check[col] = normalize_series(df_mapped[col], is_date=True)

                # Encontrar duplicados
                duplicates = []
                for idx, row in df_new_check.iterrows():
                    # Buscamos coincidencia de nombre
                    mask = (df_existing_check['name'] == row['name'])
                    
                    # Si hay coincidencia de nombre, verificamos fechas
                    if mask.any():
                        match_found = False
                        for col in date_cols:
                            if col in df_new_check.columns and col in df_existing_check.columns:
                                # Comparamos si la fecha existe en los matches de nombre
                                if any(df_existing_check.loc[mask, col] == row[col]):
                                    match_found = True
                                    break
                        if match_found:
                            duplicates.append(idx)

                if duplicates:
                    st.sidebar.warning(
                        f"⚠️ Se encontraron {len(duplicates)} posibles duplicados (mismo nombre y fecha)"
                    )
                    st.session_state.duplicate_indices = duplicates
                    
                    if st.sidebar.checkbox("Ver duplicados", key="show_dups"):
                        st.sidebar.dataframe(df_mapped.loc[duplicates][check_cols].head(10))
                    
                    # Opción para eliminar duplicados
                    if st.sidebar.button("🗑️ Eliminar duplicados y añadir"):
                        df_mapped = df_mapped.drop(index=duplicates)
                        st.sidebar.info(f"Se eliminaron {len(duplicates)} duplicados")
                        
                        # Guardar en session_state
                        if ADDITIONAL_DATA_KEY not in st.session_state:
                            st.session_state[ADDITIONAL_DATA_KEY] = []
                        
                        st.session_state[ADDITIONAL_DATA_KEY].append(df_mapped)
                        st.session_state.processed_files.add(file_id)
                        
                        st.sidebar.success("Datos añadidos (sin duplicados)!")
                        st.rerun()
            
            # Boton para confirmar (sin eliminar duplicados)
            if st.sidebar.button("✅ Confirmar y añadir datos"):
                # Guardar en session_state
                if ADDITIONAL_DATA_KEY not in st.session_state:
                    st.session_state[ADDITIONAL_DATA_KEY] = []
                
                st.session_state[ADDITIONAL_DATA_KEY].append(df_mapped)
                st.session_state.processed_files.add(file_id)
                
                st.sidebar.success("Datos añadidos correctamente!")
                st.rerun()
        
        except Exception as e:
            st.sidebar.error(f"Error al procesar CSV: {str(e)}")

