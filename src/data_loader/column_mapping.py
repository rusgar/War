"""
Mapeo inteligente de columnas entre DataFrames.
Usa similitud de cadenas para mapear columnas automaticamente.
"""

import pandas as pd
import difflib
from typing import Dict, Optional


def find_column_mapping(
    source_columns: list, target_columns: list, threshold: float = 0.6
) -> Dict[str, Optional[str]]:
    """
    Encuentra mapeo automatico entre columnas usando similitud de cadenas.
    Primero busca coincidencias exactas, luego usa similitud de secuencia,
    y finalmente usa coincidencia de palabras clave.
    
    Parameters
    ----------
    source_columns : list
        Columnas del nuevo DataFrame (CSV a agregar)
    target_columns : list
        Columnas del DataFrame original
    threshold : float
        Umbral de similitud (0-1) para considerar un match
        
    Returns
    -------
    Dict[str, Optional[str]]
        Mapeo de columna_origen -> columna_objetivo (None si no hay match)
    """
    mapping = {}
    
    for src_col in source_columns:
        # Buscar coincidencia exacta primero
        if src_col in target_columns:
            mapping[src_col] = src_col
            continue
        
        # Normalizar nombres
        src_normalized = _normalize_for_match(src_col)
        src_tokens = set(src_col.lower().replace("_", " ").split())
        
        best_match = None
        best_score = 0
        
        for tgt_col in target_columns:
            tgt_normalized = _normalize_for_match(tgt_col)
            tgt_tokens = set(tgt_col.lower().replace("_", " ").split())
            
            # Calcular puntuacion compuesta
            # 1. Similitud de secuencia (difflib)
            seq_ratio = difflib.SequenceMatcher(
                None, src_normalized, tgt_normalized
            ).ratio()
            
            # 2. Coincidencia de tokens (palabras)
            if src_tokens and tgt_tokens:
                token_overlap = len(src_tokens & tgt_tokens) / max(len(src_tokens), len(tgt_tokens))
            else:
                token_overlap = 0
            
            # 3. Coincidencia si algun token es exacto y significativo
            important_tokens = {"date", "event", "name", "age", "gender", "citizenship", 
                               "nationality", "region", "location", "killed", "death"}
            important_match = 0
            for token in src_tokens & tgt_tokens:
                if token in important_tokens:
                    important_match += 0.2
            
            # Puntuacion final (pesos)
            score = (seq_ratio * 0.4) + (token_overlap * 0.4) + min(important_match, 0.2)
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = tgt_col
        
        mapping[src_col] = best_match
    
    return mapping


def _normalize_for_match(col_name: str) -> str:
    """
    Normaliza nombre de columna para comparacion.
    Convierte a minusculas y reemplaza _ y espacios.
    """
    return col_name.lower().replace("_", "").replace(" ", "")


def apply_column_mapping(
    df_source: pd.DataFrame, mapping: Dict[str, Optional[str]]
) -> pd.DataFrame:
    """
    Aplica el mapeo de columnas al DataFrame.
    Renombra columnas y agrega columnas faltantes con None.
    
    Parameters
    ----------
    df_source : pd.DataFrame
        DataFrame origen con columnas originales
    mapping : Dict[str, Optional[str]]
        Mapeo de columna_origen -> columna_objetivo
        
    Returns
    -------
    pd.DataFrame
        DataFrame con columnas mapeadas
    """
    # Crear copia
    df = df_source.copy()
    
    # Renombrar columnas que tienen mapeo
    rename_dict = {src: tgt for src, tgt in mapping.items() if tgt is not None}
    df = df.rename(columns=rename_dict)
    
    # Identificar columnas que no se mapearon
    unmapped = [src for src, tgt in mapping.items() if tgt is None]
    
    # Eliminar columnas no mapeadas (opcional: podrian conservarse con nombre original)
    if unmapped:
        df = df.drop(columns=unmapped)
    
    return df


def get_unmapped_columns(mapping: Dict[str, Optional[str]]) -> list:
    """
    Devuelve lista de columnas que no se pudieron mapear automaticamente.
    """
    return [src for src, tgt in mapping.items() if tgt is None]
