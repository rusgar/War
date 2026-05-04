import logging
import pandas as pd
from pathlib import Path
from typing import Optional 

# El logger se configura desde logger.py - aqui solo lo obtenemos
log = logging.getLogger(__name__)

# Ruta por defecto
DATA_PATH = Path(__file__).parent.parent / "fatalities.csv"


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame: 
    """Normaliza los nombres de las columnas a snake_case.""" 
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def _apply_type_conversions(df: pd.DataFrame) -> pd.DataFrame: 
    """Aplica conversiones de tipos y limpieza de datos básicos."""
# Convertir fechas
    df["date_of_event"] = pd.to_datetime(df["date_of_event"], errors="coerce")
    df["date_of_death"] = pd.to_datetime(df["date_of_death"], errors="coerce")

# Limpiar edades
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["gender"] = df["gender"].map({"M": "Male", "F": "Female"}).fillna("Unknown") 

def _add_derived_features(df: pd.DataFrame) -> pd.DataFrame: 
    """Genera columnas calculadas (Year, Month, Age Groups)."""

    # Extraer componentes de fecha
    df["year"] = df["date_of_event"].dt.year.astype("Int32")
    df["month"] = df["date_of_event"].dt.month.astype("Int32")
    df["month_name"] = df["date_of_event"].dt.strftime("%b")

        # Clasificación por grupos
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 17, 29, 44, 59, 120],
        labels=["Minor (0-17)", "Young (18-29)", "Adult (30-44)", "Middle (45-59)", "Senior (60+)"],
        right=True,
    )

def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """
    Orquestador de la carga y limpieza del dataset.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset no encontrado en: {path}")

    log.info("Cargando dataset desde %s", path)
    df = pd.read_csv(path)
    log.info("Registros cargados: %d", len(df))

    # Pipeline de procesamiento
    df = (df.pipe(_normalize_columns)
            .pipe(_apply_type_conversions)
            .pipe(_add_derived_features))

    log.info("Dataset limpio. Columnas: %s", df.columns.tolist())
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    """
    Devuelve un diccionario con metricas resumen del dataset.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame ya cargado con load_data().

    Returns
    -------
    dict
        total_fatalities, date_range, citizenship_counts,
        avg_age, gender_counts, region_counts.
    """
    return {
        "total_fatalities": len(df),
        "date_range": (df["date_of_event"].min(), df["date_of_event"].max()),
        "citizenship_counts": df["citizenship"].value_counts().to_dict(),
        "avg_age": round(df["age"].mean(), 1),
        "gender_counts": df["gender"].value_counts().to_dict(),
        "region_counts": df["event_location_region"].value_counts().to_dict(),
    }
