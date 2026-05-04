"""
test_filters.py
===============
Tests de filters.py — RAMA feature/ui.

Meta cobertura: >= 80% de src/filters.py.
Nota: Solo testear apply_filters() y funciones puras.
      render_sidebar() usa st.* y no se testea aqui.

Commits de referencia:
  test(filters): add empty filters returns all rows
  test(filters): add year range filter test
  test(filters): add combined filters test
  test(filters): add does not modify original df test
"""

import pandas as pd
import pytest

from src.filters import apply_filters


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "year":  [2000, 2005, 2010, 2020, 2023],
        "citizenship": ["Palestinian", "Israeli", "Palestinian", "Israeli", "Palestinian"],
        "gender":      ["Male", "Female", "Male", "Male", "Female"],
        "event_location_region": ["West Bank", "Gaza Strip", "West Bank", "Israel", "West Bank"],
        "killed_by": [
            "Israeli security forces",
            "Palestinian civilians",
            "Israeli security forces",
            "Israeli security forces",
            "Palestinian civilians",
        ],
    })


@pytest.fixture
def no_filters():
    return {"year_range": None, "citizenship": [], "gender": [], "region": [], "killed_by": []}


class TestApplyFilters:

    def test_no_filters_returns_all_rows(self, sample_df, no_filters):
        pytest.skip("TODO: implementar")

    def test_year_range_filters_correctly(self, sample_df):
        pytest.skip("TODO: implementar")

    def test_year_range_excludes_outside(self, sample_df):
        pytest.skip("TODO: implementar")

    def test_citizenship_single(self, sample_df, no_filters):
        pytest.skip("TODO: implementar")

    def test_citizenship_multiple(self, sample_df, no_filters):
        pytest.skip("TODO: implementar")

    def test_gender_filter(self, sample_df, no_filters):
        pytest.skip("TODO: implementar")

    def test_region_filter(self, sample_df, no_filters):
        pytest.skip("TODO: implementar")

    def test_killed_by_filter(self, sample_df, no_filters):
        pytest.skip("TODO: implementar")

    def test_combined_filters(self, sample_df):
        # year_range=(2000,2010) + citizenship=["Palestinian"] -> 2 filas
        pytest.skip("TODO: implementar")

    def test_no_match_returns_empty_df(self, sample_df):
        pytest.skip("TODO: implementar")

    # Estos dos pasan desde el DIA 1 sin implementar nada
    def test_always_returns_dataframe(self, sample_df, no_filters):
        result = apply_filters(sample_df, no_filters)
        assert isinstance(result, pd.DataFrame)

    def test_does_not_modify_original(self, sample_df, no_filters):
        original_len = len(sample_df)
        apply_filters(sample_df, {"year_range": (2010, 2020),
                                   "citizenship": [], "gender": [],
                                   "region": [], "killed_by": []})
        assert len(sample_df) == original_len
