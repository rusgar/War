#src/stats.py

import json
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

log = logging.getLogger(__name__)

RESULTS_DIR = Path("results")


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

def fatalities_by_year_citizenship(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla pivot: filas = año, columnas = ciudadanía.[cite: 4]"""
    pivot = df.pivot_table(
        index="year", 
        columns="citizenship", 
        aggfunc="size", 
        fill_value=0
    )
    # Añadir columna "Total" por fila[cite: 4]
    pivot["Total"] = pivot.sum(axis=1)
    return pivot


def export_stats_to_json(stats: dict, output_dir: Path = RESULTS_DIR) -> Path:
    """Exporta el diccionario de estadísticas a un JSON con timestamp."""
   
    # (Paso 1): Crear directorio
    output_dir.mkdir(parents=True, exist_ok=True)

    # (Paso 2): Construir nombre del fichero
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"stats_{timestamp}.json"

    # (Paso 3 y 4): Escribir fichero
    with open(file_path, "w", encoding="utf-8") as f:
        # default=str ayuda con objetos que no son JSON-serializables directamente
        json.dump(stats, f, ensure_ascii=False, indent=2, default=str)

    log.info("Estadísticas exportadas a: %s", file_path)
    
    # (Paso 5): Devolver Path

    return file_path


def load_latest_stats(results_dir: Path = RESULTS_DIR) -> dict | None:
    """Carga el fichero de stats más reciente.[cite: 4]"""
    files = sorted(results_dir.glob("stats_*.json"))
    if not files:
        return None
    
    latest_file = files[-1]
    with open(latest_file, "r", encoding="utf-8") as f:
        return json.load(f)