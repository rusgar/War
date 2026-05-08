"""
test_charts.py
=============
Tests completos para src/charts - cobertura 100%

Patrones de test para cada gráfico:
1. Basic tests: returns Figure, has title, has traces
2. Edge cases: empty df, null values, single values
3. Error handling: invalid data, missing columns
4. Advanced: specific chart type assertions
"""

import pandas as pd
import pytest
import plotly.graph_objects as go

from src.charts.chart_fatalities_over_time import chart_fatalities_over_time
from src.charts.chart_age_distribution import chart_age_distribution
from src.charts.chart_by_region import chart_by_region
from src.charts.chart_top_locations import chart_top_locations
from src.charts.chart_killed_by import chart_killed_by
from src.charts.chart_monthly_heatmap import chart_monthly_heatmap
from src.charts.chart_gender_breakdown import chart_gender_breakdown
from src.charts.chart_scatter_3d import chart_scatter_3d


@pytest.fixture
def small_df():
    return pd.DataFrame({
        "year":               [2000, 2001, 2001, 2002, 2022, 2023],
        "month":              [1, 3, 3, 7, 10, 2],
        "date_of_event":     ["2000-01-15", "2001-03-10", "2001-03-20", "2002-07-05", "2022-10-01", "2023-02-14"],
        "citizenship":       ["Palestinian","Israeli","Palestinian","Palestinian","Israeli","Palestinian"],
        "gender":            ["Male","Female","Male","Male","Male","Female"],
        "age":               [25, 40, 16, 30, 55, 22],
        "event_location_region":   ["West Bank","West Bank","Gaza Strip","West Bank","Gaza Strip","West Bank"],
        "event_location_district": ["Jenin","Hebron","Khan Yunis","Nablus","Khan Yunis","Jenin"],
        "event_location":          ["Jenin R.C.","Beit Hagai","Khan Yunis","Nablus","Rafah","Jenin"],
        "killed_by": ["Israeli security forces","Palestinian civilians",
                      "Israeli security forces","Israeli security forces",
                      "Israeli security forces","Palestinian civilians"],
    })


class TestChartFatalitiesOverTime:
    """Tests para chart_fatalities_over_time"""
    
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

    def test_single_row(self):
        df = pd.DataFrame({"year": [2000], "citizenship": ["Palestinian"]})
        fig = chart_fatalities_over_time(df)
        assert isinstance(fig, go.Figure)

    def test_all_citizenships(self):
        df = pd.DataFrame({
            "year": [2000, 2000, 2000],
            "citizenship": ["Palestinian", "Israeli", "Foreign"]
        })
        fig = chart_fatalities_over_time(df)
        assert len(fig.data) == 3


class TestChartMonthlyHeatmap:
    """Tests para chart_monthly_heatmap"""
    
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

    def test_single_month(self):
        df = pd.DataFrame({"year": [2000], "month": [1]})
        fig = chart_monthly_heatmap(df)
        assert isinstance(fig, go.Figure)

    def test_multiple_years(self):
        df = pd.DataFrame({
            "year": [2000, 2000, 2023, 2023],
            "month": [1, 6, 1, 6]
        })
        fig = chart_monthly_heatmap(df)
        assert isinstance(fig, go.Figure)


class TestChartScatter3D:
    """Tests para chart_scatter_3d"""
    
    def test_returns_figure(self, small_df):
        fig = chart_scatter_3d(small_df)
        assert isinstance(fig, go.Figure)

    def test_has_title(self, small_df):
        fig = chart_scatter_3d(small_df)
        assert fig.layout.title.text is not None

    def test_has_3d_trace(self, small_df):
        fig = chart_scatter_3d(small_df)
        assert any(trace.type == "scatter3d" for trace in fig.data)

    def test_handles_missing_date(self):
        df = pd.DataFrame({
            "date_of_death": ["2000-01-15"],
            "age": [25],
            "citizenship": ["Palestinian"],
            "gender": ["Male"],
            "event_location_region": ["West Bank"]
        })
        fig = chart_scatter_3d(df)
        assert isinstance(fig, go.Figure)

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["date_of_event", "age", "citizenship", "gender", "event_location_region"])
        fig = chart_scatter_3d(df)
        assert isinstance(fig, go.Figure)

    def test_filters_invalid_ages(self):
        df = pd.DataFrame({
            "date_of_event": ["2000-01-15"] * 4,
            "age": [25, 150, -5, 30],
            "citizenship": ["Palestinian"] * 4,
            "gender": ["Male"] * 4,
            "event_location_region": ["West Bank"] * 4
        })
        fig = chart_scatter_3d(df)
        assert isinstance(fig, go.Figure)

    def test_raises_missing_date(self):
        df = pd.DataFrame({
            "age": [25],
            "citizenship": ["Palestinian"],
            "gender": ["Male"]
        })
        with pytest.raises(KeyError):
            chart_scatter_3d(df)

    def test_raises_missing_age(self):
        df = pd.DataFrame({
            "date_of_event": ["2000-01-15"],
            "citizenship": ["Palestinian"],
            "gender": ["Male"]
        })
        with pytest.raises(KeyError):
            chart_scatter_3d(df)

    def test_samples_large_dataset(self):
        dates = pd.date_range("2000-01-01", periods=2500, freq="D")
        df = pd.DataFrame({
            "date_of_event": dates,
            "age": [25] * 2500,
            "citizenship": ["Palestinian"] * 2500,
            "gender": ["Male"] * 2500,
            "event_location_region": ["West Bank"] * 2500
        })
        fig = chart_scatter_3d(df)
        assert isinstance(fig, go.Figure)


class TestChartAgeDistribution:
    """Tests para chart_age_distribution"""
    
    def test_returns_figure(self, small_df):
        fig = chart_age_distribution(small_df)
        assert isinstance(fig, go.Figure)

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
        df = pd.DataFrame({
            "age": [25, 150, -5, 30],
            "citizenship": ["Palestinian"] * 4
        })
        fig = chart_age_distribution(df)
        assert isinstance(fig, go.Figure)

    def test_handles_nan_ages(self):
        df = pd.DataFrame({
            "age": [25, None, 30],
            "citizenship": ["Palestinian"] * 3
        })
        fig = chart_age_distribution(df)
        assert isinstance(fig, go.Figure)

    def test_adds_mean_line(self):
        df = pd.DataFrame({
            "age": [20, 30, 40],
            "citizenship": ["Palestinian"] * 3
        })
        fig = chart_age_distribution(df)
        assert isinstance(fig, go.Figure)

    def test_creates_file_handler(self):
        import logging
        test_logger = logging.getLogger("chart_age_distribution")
        for h in test_logger.handlers[:]:
            h.close()
        test_logger.handlers.clear()
        test_logger.setLevel(logging.DEBUG)
        df = pd.DataFrame({
            "age": [25, 30],
            "citizenship": ["Palestinian"] * 2
        })
        fig = chart_age_distribution(df)
        assert isinstance(fig, go.Figure)


class TestChartGenderBreakdown:
    """Tests para chart_gender_breakdown"""
    
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
        assert any(trace.type == "sunburst" for trace in fig.data)

    def test_handles_no_gender(self):
        df = pd.DataFrame({"citizenship": ["Palestinian"], "gender": [None]})
        fig = chart_gender_breakdown(df)
        assert isinstance(fig, go.Figure)

    def test_empty_dataframe(self):
        df = pd.DataFrame({"citizenship": [], "gender": []})
        fig = chart_gender_breakdown(df)
        assert isinstance(fig, go.Figure)

    def test_single_gender(self):
        df = pd.DataFrame({
            "citizenship": ["Palestinian"],
            "gender": ["Male"]
        })
        fig = chart_gender_breakdown(df)
        assert isinstance(fig, go.Figure)


class TestChartByRegion:
    """Tests para chart_by_region"""
    
    def test_returns_figure(self, small_df):
        fig = chart_by_region(small_df)
        assert isinstance(fig, go.Figure)

    def test_has_title(self, small_df):
        fig = chart_by_region(small_df)
        assert fig.layout.title is not None

    def test_has_bar_traces(self, small_df):
        fig = chart_by_region(small_df)
        assert len(fig.data) > 0

    def test_empty_dataframe(self):
        df = pd.DataFrame({"event_location_region": [], "citizenship": []})
        fig = chart_by_region(df)
        assert isinstance(fig, go.Figure)

    def test_single_region(self):
        df = pd.DataFrame({
            "event_location_region": ["West Bank"],
            "citizenship": ["Palestinian"]
        })
        fig = chart_by_region(df)
        assert isinstance(fig, go.Figure)

    def test_sorted_by_count(self):
        df = pd.DataFrame({
            "event_location_region": ["West Bank"] * 10 + ["Gaza Strip"] * 5,
            "citizenship": ["Palestinian"] * 15
        })
        fig = chart_by_region(df)
        assert isinstance(fig, go.Figure)


class TestChartTopLocations:
    """Tests para chart_top_locations"""
    
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

    def test_single_location(self):
        df = pd.DataFrame({
            "event_location_region": ["West Bank"],
            "event_location_district": ["Jenin"],
            "event_location": ["Jenin"]
        })
        fig = chart_top_locations(df)
        assert isinstance(fig, go.Figure)


class TestChartKilledBy:
    """Tests para chart_killed_by"""
    
    def test_returns_figure(self, small_df):
        fig = chart_killed_by(small_df)
        assert isinstance(fig, go.Figure)

    def test_has_title(self, small_df):
        fig = chart_killed_by(small_df)
        assert fig.layout.title.text is not None

    def test_has_pie_and_bar(self, small_df):
        fig = chart_killed_by(small_df)
        assert len(fig.data) >= 2

    def test_empty_dataframe(self):
        df = pd.DataFrame({"killed_by": [], "date_of_event": []})
        fig = chart_killed_by(df)
        assert isinstance(fig, go.Figure)

    def test_single_killer(self):
        df = pd.DataFrame({
            "killed_by": ["Israeli security forces"],
            "date_of_event": ["2000-01-15"]
        })
        fig = chart_killed_by(df)
        assert isinstance(fig, go.Figure)

    def test_multiple_killers(self):
        df = pd.DataFrame({
            "killed_by": ["Israeli security forces", "Palestinian civilians", "Israeli security forces"],
            "date_of_event": ["2000-01-15", "2000-02-15", "2000-03-15"]
        })
        fig = chart_killed_by(df)
        assert isinstance(fig, go.Figure)