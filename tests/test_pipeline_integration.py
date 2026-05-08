"""
test_pipeline_integration.py
============================

Tests de integracion del pipeline:
    load_data -> apply_filters -> compute_descriptive_stats

Estos tests verifican que:
- load_data carga datos reales
- apply_filters filtra correctamente
- compute_descriptive_stats genera resultados coherentes
- el flujo completo no rompe con filtros reales ni con resultado vacio
"""

import pytest

from src.data_loader.load_data import load_data
from src.filters.apply_filters import apply_filters
from src.stats.compute_descriptive_stats import compute_descriptive_stats


@pytest.fixture(scope="module")
def real_df():
    """Carga el dataset real una sola vez para todo el modulo."""
    return load_data()


class TestPipelineIntegration:
    """Flujo completo: carga -> filtro -> stats."""

    def test_load_data_returns_dataframe_with_rows(self, real_df):
        assert real_df is not None
        assert hasattr(real_df, "columns")
        assert len(real_df) > 0

    def test_load_filter_stats_pipeline(self, real_df):
        filters = {
            "year_range": (2015, 2023),
            "citizenship": ["Palestinian"],
            "gender": [],
            "region": [],
            "killed_by": [],
        }

        filtered = apply_filters(real_df, filters)
        stats = compute_descriptive_stats(filtered)

        assert len(filtered) > 0
        assert isinstance(stats, dict)

        assert "total_records" in stats
        assert stats["total_records"] == len(filtered)

        assert "date_range" in stats
        assert isinstance(stats["date_range"], dict)
        assert "from" in stats["date_range"]
        assert "to" in stats["date_range"]

        assert "age_stats" in stats
        assert isinstance(stats["age_stats"], dict)

        assert "by_citizenship" in stats
        assert isinstance(stats["by_citizenship"], dict)

        assert "by_gender" in stats
        assert isinstance(stats["by_gender"], dict)

        assert "by_year" in stats
        assert isinstance(stats["by_year"], dict)

        assert "by_region" in stats
        assert isinstance(stats["by_region"], dict)

        assert "pct_minors" in stats

    def test_stats_pct_minors_is_valid_percentage(self, real_df):
        filters = {
            "year_range": (2010, 2023),
            "citizenship": [],
            "gender": [],
            "region": [],
            "killed_by": [],
        }

        filtered = apply_filters(real_df, filters)
        stats = compute_descriptive_stats(filtered)

        assert "pct_minors" in stats
        assert isinstance(stats["pct_minors"], (int, float))
        assert 0 <= stats["pct_minors"] <= 100

    def test_stats_on_empty_filtered_df_returns_zero_total(self, real_df):
        filters = {
            "year_range": (1800, 1801),
            "citizenship": [],
            "gender": [],
            "region": [],
            "killed_by": [],
        }

        filtered = apply_filters(real_df, filters)
        stats = compute_descriptive_stats(filtered)

        assert len(filtered) == 0
        assert isinstance(stats, dict)
        assert stats == {"total_records": 0}

    def test_total_records_matches_sum_by_year(self, real_df):
        filters = {
            "year_range": (2018, 2023),
            "citizenship": [],
            "gender": [],
            "region": [],
            "killed_by": [],
        }

        filtered = apply_filters(real_df, filters)
        stats = compute_descriptive_stats(filtered)

        assert stats["total_records"] == sum(stats["by_year"].values())

    def test_total_records_matches_sum_by_gender(self, real_df):
        filters = {
            "year_range": (2018, 2023),
            "citizenship": [],
            "gender": [],
            "region": [],
            "killed_by": [],
        }

        filtered = apply_filters(real_df, filters)
        stats = compute_descriptive_stats(filtered)

        assert stats["total_records"] == sum(stats["by_gender"].values())

    def test_total_records_matches_sum_by_citizenship(self, real_df):
        filters = {
            "year_range": (2018, 2023),
            "citizenship": [],
            "gender": [],
            "region": [],
            "killed_by": [],
        }

        filtered = apply_filters(real_df, filters)
        stats = compute_descriptive_stats(filtered)

        assert stats["total_records"] == sum(stats["by_citizenship"].values())
