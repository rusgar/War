"""
test_stats.py
=============
Tests de stats.py — RAMA feature/pipeline.

Meta cobertura: >= 80% de src/stats.py.

Commits de referencia:
  test(stats): add compute_descriptive_stats basic structure test
  test(stats): add pct_minors calculation test
  test(stats): add export_stats_to_json creates file test
  test(stats): add load_latest_stats returns none when empty
"""

import json
import pytest
import pandas as pd
from pathlib import Path

from src.stats import (
    compute_descriptive_stats,
    fatalities_by_year_citizenship,
    export_stats_to_json,
    load_latest_stats,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date_of_event": pd.to_datetime(["2000-01-01", "2005-06-15", "2010-03-20",
                                          "2015-11-01", "2020-07-04", "2023-10-07"]),
        "year":  [2000, 2005, 2010, 2015, 2020, 2023],
        "month": [1, 6, 3, 11, 7, 10],
        "age":   [15, 25, 40, 10, 55, 30],
        "citizenship": ["Palestinian", "Israeli", "Palestinian",
                        "Palestinian", "Israeli", "Palestinian"],
        "gender": ["Male", "Female", "Male", "Female", "Male", "Male"],
        "event_location_region": ["West Bank", "Israel", "Gaza Strip",
                                   "West Bank", "Israel", "Gaza Strip"],
    })


class TestComputeDescriptiveStats:

    def test_returns_dict(self, sample_df):
        # TODO: quitar skip e implementar
        # stats = compute_descriptive_stats(sample_df)
        # assert isinstance(stats, dict)
        pytest.skip("TODO: implementar")

    def test_total_records_correct(self, sample_df):
        # TODO: stats["total_records"] == 6
        pytest.skip("TODO: implementar")

    def test_has_required_keys(self, sample_df):
        # TODO: verificar que tiene todas las claves documentadas
        required = {"total_records", "date_range", "age_stats",
                    "by_citizenship", "by_gender", "by_year",
                    "by_region", "pct_minors"}
        pytest.skip("TODO: implementar")

    def test_pct_minors_correct(self, sample_df):
        # TODO: 2 menores de 18 sobre 6 registros -> 33.33%
        # Permitir margen: abs(stats["pct_minors"] - 33.33) < 0.1
        pytest.skip("TODO: implementar")

    def test_age_stats_mean_correct(self, sample_df):
        # TODO: media de [15,25,40,10,55,30] = 29.17 aprox
        pytest.skip("TODO: implementar")

    def test_empty_df_returns_zero_total(self):
        # TODO: compute_descriptive_stats con DataFrame vacio
        # total_records debe ser 0, pct_minors 0.0
        pytest.skip("TODO: implementar")

    def test_by_citizenship_has_keys(self, sample_df):
        pytest.skip("TODO: implementar")


class TestFatalitiesByYearCitizenship:

    def test_returns_dataframe(self, sample_df):
        pytest.skip("TODO: implementar")

    def test_has_total_column(self, sample_df):
        # TODO: la tabla pivot debe tener columna "Total"
        pytest.skip("TODO: implementar")

    def test_index_are_years(self, sample_df):
        pytest.skip("TODO: implementar")


class TestExportStatsToJson:

    def test_creates_file(self, sample_df, tmp_path):
        # TODO: export_stats_to_json(stats, output_dir=tmp_path)
        # verificar que el fichero existe
        pytest.skip("TODO: implementar")

    def test_file_is_valid_json(self, sample_df, tmp_path):
        # TODO: leer el fichero y hacer json.loads()
        pytest.skip("TODO: implementar")

    def test_filename_contains_timestamp(self, sample_df, tmp_path):
        # TODO: el nombre del fichero contiene "stats_"
        pytest.skip("TODO: implementar")

    def test_returns_path_object(self, sample_df, tmp_path):
        pytest.skip("TODO: implementar")


class TestLoadLatestStats:

    def test_returns_none_when_empty(self, tmp_path):
        # TODO: load_latest_stats(tmp_path) -> None si no hay ficheros
        pytest.skip("TODO: implementar")

    def test_returns_dict_when_file_exists(self, tmp_path):
        # TODO: crear un stats_test.json en tmp_path y verificar que lo lee
        pytest.skip("TODO: implementar")
