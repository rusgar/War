"""
test_charts.py
==============
Tests de charts.py — RAMA feature/visualization.

Meta cobertura: >= 80% de src/charts.py.
Patron: cada grafico tiene al menos 3 tests:
  1. Devuelve go.Figure
  2. Tiene titulo definido
  3. Tiene al menos un trace de datos

Commits de referencia:
  test(charts): add test_chart_fatalities_over_time suite
  test(charts): add test_chart_monthly_heatmap suite
  test(charts): add remaining chart test suites
"""

import pandas as pd
import pytest
import plotly.graph_objects as go

from src.charts import (
    chart_fatalities_over_time,
    chart_monthly_heatmap,
    chart_age_distribution,
    chart_gender_breakdown,
    chart_by_region,
    chart_top_locations,
    chart_killed_by,
)


@pytest.fixture
def small_df():
    return pd.DataFrame({
        "year":  [2000, 2001, 2001, 2002, 2022, 2023],
        "month": [1, 3, 3, 7, 10, 2],
        "citizenship": ["Palestinian","Israeli","Palestinian","Palestinian","Israeli","Palestinian"],
        "gender": ["Male","Female","Male","Male","Male","Female"],
        "age":    [25, 40, 16, 30, 55, 22],
        "event_location_region":   ["West Bank","West Bank","Gaza Strip","West Bank","Gaza Strip","West Bank"],
        "event_location_district": ["Jenin","Hebron","Khan Yunis","Nablus","Khan Yunis","Jenin"],
        "event_location":          ["Jenin R.C.","Beit Hagai","Khan Yunis","Nablus","Rafah","Jenin"],
        "killed_by": ["Israeli security forces","Palestinian civilians",
                      "Israeli security forces","Israeli security forces",
                      "Israeli security forces","Palestinian civilians"],
    })


class TestChartFatalitiesOverTime:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar")

    def test_has_title(self, small_df):
        pytest.skip("TODO: implementar")

    def test_has_traces(self, small_df):
        pytest.skip("TODO: implementar")

    # Pasa desde el Dia 1 - no tocar
    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_fatalities_over_time(pd.DataFrame({"year": [], "citizenship": []}))


class TestChartMonthlyHeatmap:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar")

    def test_has_title(self, small_df):
        pytest.skip("TODO: implementar")

    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_monthly_heatmap(pd.DataFrame({"year": [], "month": []}))


class TestChartAgeDistribution:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar")

    def test_handles_nan_ages(self):
        df = pd.DataFrame({"age": [25, None, 30], "citizenship": ["Palestinian"]*3})
        pytest.skip("TODO: implementar")

    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_age_distribution(pd.DataFrame({"age": [], "citizenship": []}))


class TestChartGenderBreakdown:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar")

    def test_has_title(self, small_df):
        pytest.skip("TODO: implementar")

    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_gender_breakdown(pd.DataFrame({"citizenship": [], "gender": []}))


class TestChartByRegion:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar")

    def test_has_title(self, small_df):
        pytest.skip("TODO: implementar")

    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_by_region(pd.DataFrame({"event_location_region": [], "citizenship": []}))


class TestChartTopLocations:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar")

    def test_has_title(self, small_df):
        pytest.skip("TODO: implementar")

    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_top_locations(pd.DataFrame({
                "event_location_region": [], "event_location_district": [], "event_location": []
            }))


class TestChartKilledBy:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar - Dia 3")

    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_killed_by(pd.DataFrame({"killed_by": []}))
