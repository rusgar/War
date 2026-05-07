#src/stats/export_stats_to_json.py

import json
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

RESULTS_DIR = Path("results")


def export_stats_to_json(stats: dict, output_dir: Path = RESULTS_DIR) -> Path:
    """Exporta el diccionario de estadísticas a un JSON con timestamp."""
   
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"stats_{timestamp}.json"

    # --- SOLUCIÓN: Convertir claves a string de forma recursiva ---
    def stringify_keys(d):
        if isinstance(d, dict):
            return {str(k): stringify_keys(v) for k, v in d.items()}
        return d
    
    clean_stats = stringify_keys(stats)
    # -------------------------------------------------------------

    with open(file_path, "w", encoding="utf-8") as f:
        # Ahora usamos clean_stats
        json.dump(clean_stats, f, ensure_ascii=False, indent=2, default=str)

    log.info("Estadísticas exportadas a: %s", file_path)
    return file_path