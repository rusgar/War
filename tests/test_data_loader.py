"""
test_data_loader.py
===================
Tests de data_loader.py — PROPORCIONADOS por el profesor.
Son la referencia de estilo para los tests que escriban los alumnos.

Ejecutar: pytest test_data_loader.py -v
(adaptad la ruta segun vuestra estructura final)
"""

import pandas as pd
import pytest
from pathlib import Path

# Adaptad este import segun vuestra estructura de carpetas
from src.data_loader import load_data, get_summary_stats


@pytest.fixture(scope="module")
def df():
    return load_data()


class TestLoadData:
    def test_returns_dataframe(self, df):
        assert isinstance(df, pd.DataFrame)

    def test_has_expected_columns(self, df):
        required = {"name", "date_of_event", "age", "citizenship", "gender", "year", "month"}
        assert required.issubset(set(df.columns))

    def test_date_of_event_is_datetime(self, df):
        assert pd.api.types.is_datetime64_any_dtype(df["date_of_event"])

    def test_year_in_valid_range(self, df):
        years = df["year"].dropna()
        assert (years >= 2000).all() and (years <= 2024).all()

    def test_age_is_numeric(self, df):
        assert pd.api.types.is_numeric_dtype(df["age"])

    def test_gender_normalized(self, df):
        assert set(df["gender"].unique()).issubset({"Male", "Female", "Unknown"})

    def test_age_group_categorical(self, df):
        assert hasattr(df["age_group"], "cat")

    def test_raises_if_file_missing(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_data(tmp_path / "noexiste.csv")

    def test_more_than_10000_rows(self, df):
        assert len(df) > 10_000


class TestGetSummaryStats:
    def test_returns_dict(self, df):
        assert isinstance(get_summary_stats(df), dict)

    def test_total_positive(self, df):
        assert get_summary_stats(df)["total_fatalities"] > 0

    def test_avg_age_reasonable(self, df):
        avg = get_summary_stats(df)["avg_age"]
        assert 5 < avg < 100

    def test_date_range_ordered(self, df):
        start, end = get_summary_stats(df)["date_range"]
        assert start < end

    def test_has_palestinian(self, df):
        assert "Palestinian" in get_summary_stats(df)["citizenship_counts"]
