"""
data_loader.py
==============
Modulo de carga y limpieza del dataset de fatalidades.

RAMA:    feature/pipeline
ESTADO:  Proporcionado por el profesor como punto de partida.
         Debeis moverlo a src/ y adaptarlo si el profesor hace un release
         que modifique su firma o comportamiento.

Dataset: B'Tselem - Israeli Information Center for Human Rights
Rango:   2000-2023  /  11.124 registros
"""

import logging
import pandas as pd
from pathlib import Path

# El logger se configura desde logger.py - aqui solo lo obtenemos
log = logging.getLogger(__name__)

# Ruta por defecto - adaptad segun vuestra estructura de carpetas
DATA_PATH = Path(__file__).parent.parent / "fatalities.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """
    Carga el CSV de fatalidades y aplica limpieza basica.

    Parameters
    ----------
    path : Path, optional
        Ruta al archivo CSV. Por defecto DATA_PATH.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio con columnas tipadas correctamente.

    Raises
    ------
    FileNotFoundError
        Si el archivo CSV no existe en la ruta indicada.

    Example
    -------
    >>> df = load_data()
    >>> len(df) > 0
    True
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset no encontrado en: {path}")

    log.info("Cargando dataset desde %s", path)
    df = pd.read_csv(path)
    log.info("Registros cargados: %d", len(df))

    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convertir fechas
    df["date_of_event"] = pd.to_datetime(df["date_of_event"], errors="coerce")
    df["date_of_death"] = pd.to_datetime(df["date_of_death"], errors="coerce")

    # Extraer year y month
    df["year"] = df["date_of_event"].dt.year.astype("Int32")
    df["month"] = df["date_of_event"].dt.month.astype("Int32")
    df["month_name"] = df["date_of_event"].dt.strftime("%b")

    # Limpiar edades
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # Estandarizar genero
    df["gender"] = df["gender"].map({"M": "Male", "F": "Female"}).fillna("Unknown")

    # Categoria de edad
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 17, 29, 44, 59, 120],
        labels=["Minor (0-17)", "Young (18-29)", "Adult (30-44)", "Middle (45-59)", "Senior (60+)"],
        right=True,
    )

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
