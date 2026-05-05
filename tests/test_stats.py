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
from src.stats.compute_descriptive_stats import compute_descriptive_stats
from src.stats.fatalities_by_year_citizenship import fatalities_by_year_citizenship
from src.stats.export_stats_to_json import export_stats_to_json
from src.stats.load_latest_stats import load_latest_stats

@pytest.fixture
def sample_df():
    """Genera un DataFrame de prueba con datos controlados."""
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
        stats = compute_descriptive_stats(sample_df)
        assert isinstance(stats, dict)

    def test_total_records_correct(self, sample_df):
        stats = compute_descriptive_stats(sample_df)
        assert stats["total_records"] == 6

    def test_has_required_keys(self, sample_df):
        stats = compute_descriptive_stats(sample_df)
        required = {"total_records", "date_range", "age_stats",
                    "by_citizenship", "by_gender", "by_year",
                    "by_region", "pct_minors"}
        assert required.issubset(stats.keys())

    def test_pct_minors_correct(self, sample_df):
        stats = compute_descriptive_stats(sample_df)
        # 2 menores (15 y 10 años) de 6 registros = 33.33%
        assert abs(stats["pct_minors"] - 33.33) < 0.1

    def test_age_stats_mean_correct(self, sample_df):
        stats = compute_descriptive_stats(sample_df)
        # Media de [15, 25, 40, 10, 55, 30] es ~29.17. El código usa round(x, 1)
        assert stats["age_stats"]["mean"] == 29.2

    def test_empty_df_returns_zero_total(self):
        df_empty = pd.DataFrame(columns=["date_of_event", "age", "citizenship", "gender", "year", "event_location_region"])
        stats = compute_descriptive_stats(df_empty)
        assert stats["total_records"] == 0

    def test_by_citizenship_has_keys(self, sample_df):
        stats = compute_descriptive_stats(sample_df)
        assert "Palestinian" in stats["by_citizenship"]
        assert "Israeli" in stats["by_citizenship"]

class TestFatalitiesByYearCitizenship:
    def test_returns_dataframe(self, sample_df):
        result = fatalities_by_year_citizenship(sample_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_total_column(self, sample_df):
        result = fatalities_by_year_citizenship(sample_df)
        assert "Total" in result.columns

    def test_index_are_years(self, sample_df):
        result = fatalities_by_year_citizenship(sample_df)
        expected_years = [2000, 2005, 2010, 2015, 2020, 2023]
        assert all(year in result.index for year in expected_years)

class TestExportStatsToJson:
    def test_creates_file(self, sample_df, tmp_path):
        stats = compute_descriptive_stats(sample_df)
        path = export_stats_to_json(stats, output_dir=tmp_path)
        assert path.exists()

    def test_file_is_valid_json(self, sample_df, tmp_path):
        stats = compute_descriptive_stats(sample_df)
        path = export_stats_to_json(stats, output_dir=tmp_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["total_records"] == 6

    def test_filename_contains_timestamp(self, sample_df, tmp_path):
        stats = compute_descriptive_stats(sample_df)
        path = export_stats_to_json(stats, output_dir=tmp_path)
        assert path.name.startswith("stats_")
        assert path.suffix == ".json"

    def test_returns_path_object(self, sample_df, tmp_path):
        stats = compute_descriptive_stats(sample_df)
        path = export_stats_to_json(stats, output_dir=tmp_path)
        assert isinstance(path, Path)

class TestLoadLatestStats:
    def test_returns_none_when_empty(self, tmp_path):
        assert load_latest_stats(tmp_path) is None

    def test_returns_dict_when_file_exists(self, tmp_path):
        dummy_stats = {"total_records": 10}
        file_path = tmp_path / "stats_20260101_120000.json"
        with open(file_path, "w") as f:
            json.dump(dummy_stats, f)
        
        loaded = load_latest_stats(tmp_path)
        assert loaded["total_records"] == 10