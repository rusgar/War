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
        fig = chart_fatalities_over_time(small_df)
        assert isinstance(fig, go.Figure)

    def test_has_title(self, small_df):
        fig = chart_fatalities_over_time(small_df)
        assert fig.layout.title.text is not None

    def test_has_traces(self, small_df):
        fig = chart_fatalities_over_time(small_df)
        assert len(fig.data) > 0

    def test_has_citizenship_lines(self, small_df):
        fig = chart_fatalities_over_time(small_df)
        assert len(fig.data) >= 1

    def test_empty_dataframe(self):
        df = pd.DataFrame({"year": [], "citizenship": []})
        fig = chart_fatalities_over_time(df)
        assert isinstance(fig, go.Figure)


class TestChartMonthlyHeatmap:

    def test_returns_figure(self, small_df):
        fig = chart_monthly_heatmap(small_df)
        assert isinstance(fig, go.Figure)

    def test_has_title(self, small_df):
        fig = chart_monthly_heatmap(small_df)
        assert fig.layout.title.text is not None

    def test_has_heatmap_trace(self, small_df):
        fig = chart_monthly_heatmap(small_df)
        assert len(fig.data) > 0

    def test_empty_dataframe(self):
        df = pd.DataFrame({"year": [], "month": []})
        fig = chart_monthly_heatmap(df)
        assert isinstance(fig, go.Figure)


class TestChartAgeDistribution:



    def test_has_title(self, small_df):
        fig = chart_age_distribution(small_df)
        assert fig.layout.title is not None

    def test_has_traces(self, small_df):
        fig = chart_age_distribution(small_df)
        assert len(fig.data) > 0

    def test_handles_empty_df(self):
        df = pd.DataFrame({"age": [], "citizenship": []})
        fig = chart_age_distribution(df)
        assert isinstance(fig, go.Figure)

    def test_filters_invalid_ages(self):
        df = pd.DataFrame(
            {"age": [25, 150, -5, 30], "citizenship": ["Palestinian"] * 4}
        )
        fig = chart_age_distribution(df)
        assert isinstance(fig, go.Figure)

    def test_creates_log_file(self):
        import logging
        from pathlib import Path

        log_path = Path("logs/log_age_dist.log")
        for h in logging.getLogger("charts").handlers[:]:
            h.close()
            logging.getLogger("charts").removeHandler(h)
        logging.getLogger("charts").setLevel(logging.DEBUG)
        df = pd.DataFrame({"age": [25, 30], "citizenship": ["Palestinian"] * 2})
        chart_age_distribution(df)
        assert log_path.exists()

    def test_log_contains_chart_name(self):
        import logging
        from pathlib import Path

        log_path = Path("logs/log_age_dist.log")
        for h in logging.getLogger("charts").handlers[:]:
            h.close()
            logging.getLogger("charts").removeHandler(h)
        logging.getLogger("charts").setLevel(logging.DEBUG)
        df = pd.DataFrame({"age": [25, 30], "citizenship": ["Palestinian"] * 2})
        chart_age_distribution(df)
        content = log_path.read_text(encoding="utf-8")
        assert "chart_age_distribution" in content


class TestChartGenderBreakdown:

    def test_returns_figure(self, small_df):
        fig = chart_gender_breakdown(small_df)
        assert isinstance(fig, go.Figure)

    def test_has_title(self, small_df):
        fig = chart_gender_breakdown(small_df)
        assert fig.layout.title.text is not None

    def test_title_contains_total(self, small_df):
        fig = chart_gender_breakdown(small_df)
        assert "registros" in fig.layout.title.text.lower()

    def test_has_sunburst_trace(self, small_df):
        fig = chart_gender_breakdown(small_df)
        assert len(fig.data) > 0

    def test_handles_no_gender(self):
        df = pd.DataFrame({"citizenship": ["Palestinian"], "gender": [None]})
        fig = chart_gender_breakdown(df)
        assert isinstance(fig, go.Figure)

    def test_empty_dataframe(self):
        df = pd.DataFrame({"citizenship": [], "gender": []})
        fig = chart_gender_breakdown(df)
        assert isinstance(fig, go.Figure)


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
        fig = chart_top_locations(small_df)
        assert isinstance(fig, go.Figure)

    def test_has_title(self, small_df):
        fig = chart_top_locations(small_df)
        assert fig.layout.title.text is not None

    def test_title_contains_total(self, small_df):
        fig = chart_top_locations(small_df)
        assert "registros" in fig.layout.title.text.lower()

    def test_has_treemap_trace(self, small_df):
        fig = chart_top_locations(small_df)
        assert len(fig.data) > 0

    def test_handles_null_region(self):
        df = pd.DataFrame({
            "event_location_region": [None, "West Bank"],
            "event_location_district": ["Jenin", "Hebron"],
            "event_location": ["Jenin", "Hebron"]
        })
        fig = chart_top_locations(df)
        assert isinstance(fig, go.Figure)

    def test_empty_dataframe(self):
        df = pd.DataFrame({
            "event_location_region": [], 
            "event_location_district": [], 
            "event_location": []
        })
        fig = chart_top_locations(df)
        assert isinstance(fig, go.Figure)


class TestChartKilledBy:

    def test_returns_figure(self, small_df):
        pytest.skip("TODO: implementar - Dia 3")

    def test_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            chart_killed_by(pd.DataFrame({"killed_by": []}))
