#src/stats/compute_descriptive_stats.py

import logging

import pandas as pd

log = logging.getLogger(__name__)

def compute_descriptive_stats(df: pd.DataFrame) -> dict:
    """
    Calcula estadisticas descriptivas completas sobre el DataFrame.
    """
    if df.empty:
        log.warning("Se intentó calcular estadísticas sobre un DataFrame vacío.")
        return {"total_records": 0}
    
    # (Paso 1): total_records
    total_records = len(df)

    # (Paso 2): date_range (Manejo de NaT)
    min_date = df["date_of_event"].min()
    max_date = df["date_of_event"].max()
    
    date_range = {
        "from": min_date.isoformat() if pd.notnull(min_date) else None,
        "to": max_date.isoformat() if pd.notnull(max_date) else None
    }

    # (Paso 3): age_stats
    age_stats = {
        "mean": round(df["age"].mean(), 1),
        "median": round(df["age"].median(), 1),
        "std": round(df["age"].std(), 1),
        "min": float(df["age"].min()),
        "max": float(df["age"].max())
    }

    # (Paso 4): Agrupaciones por categorías
    stats = {
        "total_records": total_records,
        "date_range": date_range,
        "age_stats": age_stats,
        "by_citizenship": df["citizenship"].value_counts().to_dict(),
        "by_gender": df["gender"].value_counts().to_dict(),
        "by_year": df["year"].value_counts().sort_index().to_dict(),
        "by_region": df["event_location_region"].value_counts().to_dict(),
    }

    # (Paso 5): pct_minors
    stats["pct_minors"] = round((df["age"] < 18).sum() / total_records * 100, 2) if total_records > 0 else 0.0

    return stats

