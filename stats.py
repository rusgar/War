"""
stats.py
========
Modulo de estadisticas descriptivas y exportacion de resultados.

RAMA:    feature/pipeline
ALUMNO:  El que tenga pipeline ese dia
TAREA:   Implementar las funciones de analisis y exportacion.

El objetivo de este modulo es doble:
  1. Calcular estadisticas relevantes del dataset (filtrado o completo).
  2. Exportar esas estadisticas a results/stats_YYYYMMDD.json
     para que quede registro de cada ejecucion.

Commits de referencia:
  feat(stats): implement compute_descriptive_stats
  feat(stats): implement export_stats_to_json
  feat(stats): add fatalities_by_year_citizenship aggregation
  test(stats): add test_compute_descriptive_stats with sample data
  docs(stats): update stats.md
"""

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

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado o completo.

    Returns
    -------
    dict
        Diccionario con las siguientes claves:
          - total_records (int)
          - date_range (dict con "from" y "to" como strings ISO)
          - age_stats (dict: mean, median, std, min, max)
          - by_citizenship (dict: ciudadania -> conteo)
          - by_gender (dict: genero -> conteo)
          - by_year (dict: anio -> conteo)
          - by_region (dict: region -> conteo)
          - pct_minors (float): % de menores de 18

    Example
    -------
    >>> stats = compute_descriptive_stats(df)
    >>> stats["total_records"] > 0
    True
    """
    # TODO (Paso 1): total_records = len(df)

    # TODO (Paso 2): date_range con min y max de date_of_event
    # Hint: df["date_of_event"].min().isoformat() si no es NaT

    # TODO (Paso 3): age_stats con df["age"].describe()
    # Incluir: mean, median (df["age"].median()), std, min, max
    # Redondear a 1 decimal. Manejar NaN con skipna=True.

    # TODO (Paso 4): by_citizenship, by_gender, by_year, by_region
    # Hint: df["citizenship"].value_counts().to_dict()

    # TODO (Paso 5): pct_minors
    # Hint: (df["age"] < 18).sum() / len(df) * 100 si len(df) > 0 else 0.0

    raise NotImplementedError("compute_descriptive_stats pendiente de implementar")


def fatalities_by_year_citizenship(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tabla pivot: filas = anio, columnas = ciudadania, valores = conteo.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Tabla pivot lista para mostrar o exportar.

    Hints
    -----
    - Agrupa por ["year", "citizenship"] y cuenta.
    - Pivota con .pivot_table(index="year", columns="citizenship",
      aggfunc="size", fill_value=0).
    - Aniade columna "Total" con la suma de cada fila.
    """
    # TODO: implementar
    raise NotImplementedError("fatalities_by_year_citizenship pendiente")


def export_stats_to_json(stats: dict, output_dir: Path = RESULTS_DIR) -> Path:
    """
    Exporta el diccionario de estadisticas a un JSON con timestamp.

    El nombre del fichero incluye la fecha: stats_YYYYMMDD_HHMMSS.json

    Parameters
    ----------
    stats : dict
        Diccionario devuelto por compute_descriptive_stats().
    output_dir : Path
        Directorio donde guardar el fichero.

    Returns
    -------
    Path
        Ruta del fichero creado.

    Example
    -------
    >>> path = export_stats_to_json(stats)
    >>> path.exists()
    True
    """
    # TODO (Paso 1): output_dir.mkdir(parents=True, exist_ok=True)

    # TODO (Paso 2): Construir nombre con datetime.now().strftime(...)

    # TODO (Paso 3): json.dumps(stats, ensure_ascii=False, indent=2, default=str)
    # El default=str maneja fechas y otros tipos no serializables

    # TODO (Paso 4): Escribir fichero y hacer log.info con la ruta

    # TODO (Paso 5): Devolver el Path del fichero creado

    raise NotImplementedError("export_stats_to_json pendiente de implementar")


def load_latest_stats(results_dir: Path = RESULTS_DIR) -> dict | None:
    """
    Carga el fichero de stats mas reciente del directorio results/.

    Parameters
    ----------
    results_dir : Path

    Returns
    -------
    dict | None
        Diccionario de stats o None si no hay ningun fichero.

    Hints
    -----
    - Usar sorted(results_dir.glob("stats_*.json")) y coger el ultimo.
    - json.loads(path.read_text(encoding="utf-8"))
    """
    # TODO: implementar
    raise NotImplementedError("load_latest_stats pendiente")
