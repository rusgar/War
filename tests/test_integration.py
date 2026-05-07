"""
test_integration.py
===================
Tests de integracion — ROL REVIEWER (el alumno sin rama ese dia).

Estos tests verifican que los modulos funcionan JUNTOS correctamente:
  - Filtros -> graficos no crashean con datos vacios
  - data_loader -> stats funciona sobre datos reales
  - apply_filters -> kpis devuelven valores coherentes

No testean implementaciones internas, testean el flujo completo.

El reviewer actualiza este fichero cada dia segun lo que se haya
implementado ese dia. Al final del Dia 4 debe estar completo.

Commits de referencia:
  test(integration): add filters to empty dataframe does not crash charts
  test(integration): add full pipeline load -> filter -> stats test
  test(integration): add kpis delta is non-positive when filtered
"""

import pandas
import pytest

# Importaciones que iran activandose segun avance el ejercicio
from src.data_loader.load_data import load_data
from src.filters.apply_filters import apply_filters


@pytest.fixture(scope="module")
def real_df():
    """Dataset real cargado una sola vez para todos los tests de integracion."""
    return load_data()


@pytest.fixture
def empty_filters():
    return {"year_range": None, "citizenship": [], "gender": [], "region": [], "killed_by": []}


class TestFiltersWithRealData:

    def test_no_filters_returns_full_dataset(self, real_df, empty_filters):
        result = apply_filters(real_df, empty_filters)
        assert len(result) == len(real_df)

    def test_filter_reduces_rows(self, real_df):
        filters = {"year_range": (2020, 2023), "citizenship": ["Palestinian"],
                   "gender": [], "region": [], "killed_by": []}
        result = apply_filters(real_df, filters)
        assert len(result) < len(real_df)
        assert len(result) > 0

    def test_impossible_filter_returns_empty(self, real_df):
        filters = {"year_range": (1800, 1801), "citizenship": [],
                   "gender": [], "region": [], "killed_by": []}
        result = apply_filters(real_df, filters)
        assert len(result) == 0

    def test_filtered_df_has_same_columns(self, real_df, empty_filters):
        result = apply_filters(real_df, empty_filters)
        assert set(result.columns) == set(real_df.columns)


class TestChartsWithEmptyData:
    """
    Verificar que los graficos no crashean con DataFrames vacios.
    Activar cuando feature/visualization este implementada.
    """

    def test_fatalities_over_time_empty_df(self):
        # TODO: activar cuando chart_fatalities_over_time este implementada
        # from src.charts import chart_fatalities_over_time
        # empty = pd.DataFrame({"year": [], "citizenship": []})
        # No debe lanzar excepcion (NotImplementedError SI es aceptable)
        pytest.skip("Activar en Dia 2")

    def test_all_charts_accept_empty_df(self):
        pytest.skip("Activar en Dia 2")


class TestPipelineIntegration:
    """
    Flujo completo: carga -> filtro -> stats.
    Activar cuando feature/pipeline este implementada.
    """

    def test_load_filter_stats_pipeline(self, real_df):
        # TODO: activar cuando compute_descriptive_stats este implementada
        # from src.stats import compute_descriptive_stats
        # filters = {"year_range": (2015, 2023), ...}
        # filtered = apply_filters(real_df, filters)
        # stats = compute_descriptive_stats(filtered)
        # assert stats["total_records"] == len(filtered)
        pytest.skip("Activar en Dia 2")

    def test_stats_pct_minors_is_valid_percentage(self, real_df):
        pytest.skip("Activar en Dia 2")


class TestKpisCoherence:
    """
    Verificar que los KPIs tienen sentido logico.
    Activar cuando feature/ui (kpis) este implementada.
    """

    def test_filtered_total_le_original(self, real_df):
        # TODO: activar cuando _calc_* esten implementadas
        # El total filtrado nunca puede superar el original
        pytest.skip("Activar en Dia 2")
