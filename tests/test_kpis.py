"""
test_kpis.py
============
Tests de kpis.py — RAMA feature/ui.

Estrategia:
- Testear _calc_*() directamente (funciones puras).
- Mockear st con unittest.mock para testear render_kpis().

Meta cobertura: >= 80% de src/kpis.py.
"""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.kpis import (
    _calc_pct_minors,
    _calc_years_covered,
    _calc_regions,
    _calc_avg_age,
    render_kpis,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "age":   [10, 25, 35, 15, 50],
        "year":  [2000, 2005, 2010, 2015, 2020],
        "event_location_region": ["West Bank", "Gaza Strip", "Israel", "West Bank", "Gaza Strip"],
    })


class TestCalcPctMinors:

    def test_correct_percentage(self, sample_df):
        # 2 menores (10, 15) sobre 5 total -> 40.0%
        pytest.skip("TODO: implementar")

    def test_empty_df_returns_zero(self):
        empty = pd.DataFrame({"age": []})
        pytest.skip("TODO: implementar")

    def test_no_minors(self):
        df = pd.DataFrame({"age": [20, 30, 40]})
        pytest.skip("TODO: implementar")

    def test_all_minors(self):
        df = pd.DataFrame({"age": [5, 10, 15]})
        pytest.skip("TODO: implementar")


class TestCalcYearsCovered:

    def test_correct_count(self, sample_df):
        # sample_df tiene 5 anios distintos
        pytest.skip("TODO: implementar")

    def test_empty_returns_zero(self):
        pytest.skip("TODO: implementar")

    def test_duplicate_years_counted_once(self):
        df = pd.DataFrame({"year": [2000, 2000, 2001, 2001]})
        pytest.skip("TODO: implementar")


class TestCalcRegions:

    def test_correct_count(self, sample_df):
        # West Bank, Gaza Strip, Israel -> 3 regiones
        pytest.skip("TODO: implementar")

    def test_empty_returns_zero(self):
        pytest.skip("TODO: implementar")


class TestCalcAvgAge:

    def test_correct_average(self, sample_df):
        # (10+25+35+15+50)/5 = 27.0
        pytest.skip("TODO: implementar")

    def test_empty_returns_zero(self):
        pytest.skip("TODO: implementar")

    def test_ignores_nan(self):
        df = pd.DataFrame({"age": [10, None, 30]})
        pytest.skip("TODO: implementar")


class TestRenderKpis:

    @patch("src.kpis.st")
    def test_creates_five_columns(self, mock_st, sample_df):
        # Configurar mock_st.columns para devolver 5 mocks
        # Verificar que mock_st.columns fue llamado con 5
        pytest.skip("TODO: implementar")

    @patch("src.kpis.st")
    def test_calls_metric_five_times(self, mock_st, sample_df):
        pytest.skip("TODO: implementar")

    @patch("src.kpis.st")
    def test_handles_empty_filtered_df(self, mock_st, sample_df):
        # No debe lanzar excepcion con df vacio
        empty = sample_df.iloc[0:0]
        pytest.skip("TODO: implementar")
