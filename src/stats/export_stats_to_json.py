#src/stats/export_stats_to_json.py

import json
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

RESULTS_DIR = Path("results")


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

