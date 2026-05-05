#src/stats/load_latest_stats.py

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

RESULTS_DIR = Path("results")


def load_latest_stats(results_dir: Path = RESULTS_DIR) -> dict | None:
    """Carga el fichero de stats más reciente.[cite: 4]"""
    files = sorted(results_dir.glob("stats_*.json"))
    if not files:
        return None
    
    latest_file = files[-1]
    with open(latest_file, "r", encoding="utf-8") as f:
        return json.load(f)