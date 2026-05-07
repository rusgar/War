# Documentación de Tests - Charts
**Autor:** Carlos
**Fecha:** 06/05/2026

---

## Resumen

Este archivo contiene los tests unitarios para el módulo `src/charts`. 
Cobertura: **100%**

Total de tests: **56**

---

## Estructura de Tests

Cada gráfico tiene:
- Tests básicos: devuelve Figure, tiene título, tiene traces
- Tests de edge cases: DataFrame vacío, valores nulos, un solo valor
- Tests de error: verifica que lance excepciones cuando corresponde

---

## Fixture: small_df

DataFrame de ejemplo usado en todos los tests:

| Columna | Valores |
|--------|--------|
| year | 2000, 2001, 2001, 2002, 2022, 2023 |
| month | 1, 3, 3, 7, 10, 2 |
| date_of_event | 2000-01-15, 2001-03-10, ... |
| citizenship | Palestinian, Israeli |
| gender | Male, Female |
| age | 25, 40, 16, 30, 55, 22 |
| event_location_region | West Bank, Gaza Strip |
| killed_by | Israeli security forces, Palestinian civilians |

---

## Tests por Gráfico

### 1. TestChartFatalitiesOverTime (7 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_has_traces | Verifica que tiene datos |
| test_has_citizenship_lines | Verifica líneas por ciudadanía |
| test_empty_dataframe | Maneja DataFrame vacío |
| test_single_row | Maneja un solo dato |
| test_all_citizenships | Funciona con 3 ciudadanías |

---

### 2. TestChartMonthlyHeatmap (6 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_has_heatmap_trace | Verifica heatmap trace |
| test_empty_dataframe | Maneja DataFrame vacío |
| test_single_month | Maneja un solo mes |
| test_multiple_years | Varios años |

---

### 3. TestChartScatter3D (10 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_has_3d_trace | Verifica trace 3D |
| test_handles_missing_date | Usa date_of_death si no hay date_of_event |
| test_empty_dataframe | Maneja DataFrame vacío |
| test_filters_invalid_ages | Filtra edades inválidas |
| test_raises_missing_date | Lanza KeyError si no hay fecha |
| test_raises_missing_age | Lanza KeyError si no hay edad |
| test_samples_large_dataset | Muestrea si >2000 datos |

---

### 4. TestChartAgeDistribution (8 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_has_traces | Verifica que tiene traces |
| test_handles_empty_df | Maneja DataFrame vacío |
| test_filters_invalid_ages | Filtra edades 0-110 |
| test_handles_nan_ages | Maneja edades NaN |
| test_adds_mean_line | Añade línea de media |
| test_creates_file_handler | Crea handler de log |

---

### 5. TestChartGenderBreakdown (7 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_title_contains_total | Título tiene "registros" |
| test_has_sunburst_trace | Verifica trace sunburst |
| test_handles_no_gender | Maneja gender nulo |
| test_empty_dataframe | Maneja DataFrame vacío |
| test_single_gender | Un solo género |

---

### 6. TestChartByRegion (6 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_has_bar_traces | Verifica traces de barras |
| test_empty_dataframe | Maneja DataFrame vacío |
| test_single_region | Una sola región |
| test_sorted_by_count | Ordenado por cantidad |

---

### 7. TestChartTopLocations (7 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_title_contains_total | Título tiene "registros" |
| test_has_treemap_trace | Verifica treemap |
| test_handles_null_region | Maneja región nula |
| test_empty_dataframe | Maneja DataFrame vacío |
| test_single_location | Una sola ubicación |

---

### 8. TestChartKilledBy (6 tests)

| Test | Descripción |
|------|------------|
| test_returns_figure | Verifica que devuelve go.Figure |
| test_has_title | Verifica que tiene título |
| test_has_pie_and_bar | Tiene pie + barras |
| test_empty_dataframe | Maneja DataFrame vacío |
| test_single_killer | Un solo killer |
| test_multiple_killers | Varios killers |

---

## Cómo Ejecutar

```bash
# Todos los tests
pytest tests/test_charts.py -v

# Con cobertura
pytest tests/test_charts.py --cov=src/charts --cov-report=term-missing
```

---

## Resultados Actuales

- **56 tests passed**
- **100% cobertura**
- **0 failures**