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

from src.filters.apply_filters import apply_filters


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
        result = apply_filters(sample_df, no_filters)
        assert len(result) == len(sample_df)

    def test_year_range_filters_correctly(self, sample_df):
        filters = {"year_range": (2000, 2010), "citizenship": [], "gender": [], "region": [], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 3
        assert all((2000 <= y <= 2010) for y in result["year"])

    def test_year_range_excludes_outside(self, sample_df):
        filters = {"year_range": (2005, 2005), "citizenship": [], "gender": [], "region": [], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 1
        assert result["year"].iloc[0] == 2005

    def test_citizenship_single(self, sample_df, no_filters):
        filters = {"year_range": None, "citizenship": ["Palestinian"], "gender": [], "region": [], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 3
        assert all(c == "Palestinian" for c in result["citizenship"])

    def test_citizenship_multiple(self, sample_df, no_filters):
        filters = {"year_range": None, "citizenship": ["Palestinian", "Israeli"], "gender": [], "region": [], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 5

    def test_gender_filter(self, sample_df, no_filters):
        filters = {"year_range": None, "citizenship": [], "gender": ["Male"], "region": [], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 3
        assert all(g == "Male" for g in result["gender"])

    def test_region_filter(self, sample_df, no_filters):
        filters = {"year_range": None, "citizenship": [], "gender": [], "region": ["West Bank"], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 3

    def test_killed_by_filter(self, sample_df, no_filters):
        filters = {"year_range": None, "citizenship": [], "gender": [], "region": [], "killed_by": ["Israeli security forces"]}
        result = apply_filters(sample_df, filters)
        assert len(result) == 3

    def test_combined_filters(self, sample_df):
        filters = {"year_range": (2000, 2010), "citizenship": ["Palestinian"], "gender": [], "region": [], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 2

    def test_no_match_returns_empty_df(self, sample_df):
        filters = {"year_range": (1900, 1950), "citizenship": [], "gender": [], "region": [], "killed_by": []}
        result = apply_filters(sample_df, filters)
        assert len(result) == 0

    def test_always_returns_dataframe(self, sample_df, no_filters):
        result = apply_filters(sample_df, no_filters)
        assert isinstance(result, pd.DataFrame)

    def test_does_not_modify_original(self, sample_df, no_filters):
        original_len = len(sample_df)
        apply_filters(sample_df, {"year_range": (2010, 2020),
                                   "citizenship": [], "gender": [],
                                   "region": [], "killed_by": []})
        assert len(sample_df) == original_len

    def test_handles_nan_ages(self):
        df = pd.DataFrame({"age": [25, None, 30], "citizenship": ["Palestinian"]*3})
        filters = {"year_range": None, "citizenship": ["Palestinian"], "gender": [], "region": [], "killed_by": []}
        result = apply_filters(df, filters)
        assert len(result) == 3
