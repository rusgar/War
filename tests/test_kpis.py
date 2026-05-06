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

from src.kpis.kpis import (
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
        result = _calc_pct_minors(sample_df)
        assert result == 40.0

    def test_empty_df_returns_zero(self):
        empty = pd.DataFrame({"age": []})
        assert _calc_pct_minors(empty) == 0.0

    def test_no_minors(self):
        df = pd.DataFrame({"age": [20, 30, 40]})
        assert _calc_pct_minors(df) == 0.0

    def test_all_minors(self):
        df = pd.DataFrame({"age": [5, 10, 15]})
        assert _calc_pct_minors(df) == 100.0


class TestCalcYearsCovered:

    def test_correct_count(self, sample_df):
        result = _calc_years_covered(sample_df)
        assert result == 5

    def test_empty_returns_zero(self):
        empty = pd.DataFrame({"year": []})
        assert _calc_years_covered(empty) == 0

    def test_duplicate_years_counted_once(self):
        df = pd.DataFrame({"year": [2000, 2000, 2001, 2001]})
        assert _calc_years_covered(df) == 2


class TestCalcRegions:

    def test_correct_count(self, sample_df):
        result = _calc_regions(sample_df)
        assert result == 3

    def test_empty_returns_zero(self):
        empty = pd.DataFrame({"event_location_region": []})
        assert _calc_regions(empty) == 0


class TestCalcAvgAge:

    def test_correct_average(self, sample_df):
        result = _calc_avg_age(sample_df)
        assert result == 27.0

    def test_empty_returns_zero(self):
        empty = pd.DataFrame({"age": []})
        assert _calc_avg_age(empty) == 0.0

    def test_ignores_nan(self):
        df = pd.DataFrame({"age": [10, None, 30]})
        assert _calc_avg_age(df) == 20.0


class TestRenderKpis:

    @patch("src.kpis.kpis.st")
    def test_creates_five_columns(self, mock_st, sample_df):
        mock_cols = [MagicMock() for _ in range(5)]
        mock_st.columns.return_value = mock_cols
        df_original = sample_df.copy()
        render_kpis(sample_df, df_original)
        mock_st.columns.assert_called_with(5)

    @patch("src.kpis.kpis.st")
    def test_calls_metric_five_times(self, mock_st, sample_df):
        mock_cols = [MagicMock() for _ in range(5)]
        mock_st.columns.return_value = mock_cols
        df_original = sample_df.copy()
        render_kpis(sample_df, df_original)
        assert mock_cols[0].metric.call_count == 1
        assert mock_cols[1].metric.call_count == 1
        assert mock_cols[2].metric.call_count == 1
        assert mock_cols[3].metric.call_count == 1
        assert mock_cols[4].metric.call_count == 1

    @patch("src.kpis.kpis.st")
    def test_handles_empty_filtered_df(self, mock_st, sample_df):
        mock_cols = [MagicMock() for _ in range(5)]
        mock_st.columns.return_value = mock_cols
        empty = sample_df.iloc[0:0]
        render_kpis(empty, sample_df)
