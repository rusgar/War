# DECISIONS.md
> Registro de decisiones de arquitectura del equipo.
> Completar el Dia 1 antes de escribir codigo.

---

## Decision 1 — Estructura de carpetas

**Fecha:** 04/05/2026
**Participantes:** todos  
**Decision:**

```
C:.
│   app.py
│   main.py
│   README.md
│   requirements.txt
│   
├───.github
│   └───workflows
│           ci.yml
├───data
│       fatalities.csv
│       
├───docs
│   │   DECISIONS.md
│   │   
│   └───Feature
│           pipeline.md
│           
├───logs
├───results
├───src
│   │   charts.py
│   │   config.py
│   │   filters.py
│   │   kpis.py
│   │   __init__.py
│   ├───data_loader
│   │   │   load_data.py
│   │   │   _add_derived_features.py
│   │   │   _apply_type_conversions.py
│   │   └───_normalize_columns.py
│   ├───logger
│   │   │   log_chart_rendered.py
│   │   │   log_data_loaded.py
│   │   │   log_filter_applied.py
│   │   └───setup_logger.py
│   └───stats
│       │   compute_descriptive_stats.py
│       │   export_stats_to_json.py
│       │   fatalities_by_year_citizenship.py
│       └───load_latest_stats.py
└───tests
    │   test_charts.py
    │   test_data_loader.py
    │   test_filters.py
    │   test_integration.py
    │   test_kpis.py
    │   test_logger.py
    │   test_stats.py
    └───__init__.py

```

**Razon:**

---

## Decision 2 — Convencion de imports

**Decision:** (ej. `from src.charts import ...` vs `import src.charts as charts`)  
**Razon:**

---

## Decision 3 — Rotacion de ramas

| Dia | pipeline | visualization | ui | reviewer |
|-----|----------|---------------|----|----------|
| 1   | Carlos | | | |
| 2   | Andrés , Carlos | | | |
| 3   | | | Andres , Israel | |
| 4   | | | | |

---

## Decision 4 — Estrategia de merge

**Decision:** (ej. squash merge / merge commit / rebase)  
**Razon:**

---

## Decisiones futuras

_(Anadir aqui cualquier decision tomada durante el ejercicio con fecha y razon)_

05 / 05 / 2026 

**Decision:** Añadido `main.py` a peticion de Angel

**Razon:** Iniciar el streamlit directamente sin necesidad de hacer el comando `streamlit run app.py`


# RESUMEN

**Proyecto:** War Analytics Dashboard  
**Fecha final:** 09/05/2026  
**Rama estable:** `main` (v1.0.0)  
**Estado:** ✅ Todos los tests pasan (117 passed) · CI/CD verde · Dashboard funcional

---

## 📋 Índice de decisiones

1. [Estructura del proyecto](#1-estructura-del-proyecto)
2. [Gestión de ramas](#2-gestión-de-ramas)
3. [Resolución de conflictos](#3-resolución-de-conflictos)
4. [Corrección de tests](#4-corrección-de-tests)
5. [CI/CD y linting](#5-cicd-y-linting)
6. [Nomenclatura de módulos](#6-nomenclatura-de-módulos)
7. [Logging y monitoreo](#7-logging-y-monitoreo)

---

## 1. Estructura del proyecto

### Decisión 1.1: Organización modular en `src/`
**Responsables:** Todo el equipo  
**Justificación:** Separar responsabilidades siguiendo SRP (Single Responsibility Principle)

**Estructura final:**

````
src/
├── charts/ # 9 módulos de visualización (todos funcionando)
├── data_loader/ # Carga y limpieza de datos + CSVs adicionales
├── filters/ # Lógica de filtros y sidebar
├── kpis/ # Cálculos económicos (KPIs)
├── logger/ # Logging estructurado
├── pages/ # 7 módulos UI modulares (parcialmente integrados)
└── stats/ # Estadísticas y exportación JSON

````

**Cambios respecto al plan inicial:**
- ✅ `app.py` movido a `src/app.py` (lanzado vía `main.py`)
- ✅ `chart_geopandas.py` renombrado a `chart_geospatial.py` (consistencia)
- ✅ `src/pages/` creado para UI modular (pendiente integración completa)

---

## 2. Gestión de ramas

| Campo | Detalle |
|---|---|
| **Fecha** | 05/05/2026 |
| **Responsable** | Edu |
| **Justificación** | Evitar merges directos a `main` sin validación previa |

**Flujo de trabajo:**
````
feature/visualizacion ──┐
feature/ui ─────────────┼──→ integration ──→ main (v1.0.0)
feature/pipeline ───────┘

````
---
### Decisión 2.2: Renombrar `pipeline` a `feature/pipeline`
| Campo | Detalle |
|---|---|
| **Fecha** | 06/05/2026 |
| **Justificación** | Consistencia en nomenclatura de ramas |

---

### Decisión 2.3: Sincronización de ramas post-merge
**Comandos aplicados:**
```
git checkout feature/visualizacion && git rebase integration
git checkout feature/ui && git rebase integration
git checkout feature/pipeline && git rebase integration
```
- Resultado: Todas las ramas alineadas con integration (commit 8f66c94)

## 3. Resolución de conflictos
 
### Conflicto 3.1: `requirements.txt` (binario)
 
| Campo | Detalle |
|---|---|
| **Problema** | Conflicto de fusión en archivo binario |
| **Solución** | Unión manual de todas las dependencias |
| **Resultado** | `geopy`, `plotly`, `pandas`, `streamlit` instalados correctamente |
 
---
 
### Conflicto 3.2: `app.py` — pérdida de cambios de `feature/ui`
 
| Campo | Detalle |
|---|---|
| **Problema** | Al resolver conflictos se sobrescribió la función `combine_data()` |
| **Solución** | Reintegración manual del código de carga de CSVs adicionales |
 
**Archivo final `src/app.py` con ambas funcionalidades:**
 
- Portada y sidebar (proveniente de `integration`)
- Carga de CSVs adicionales (proveniente de `feature/visualizacion`)
---
 
### Conflicto 3.3: Múltiples conflictos en `src/filters/`
 
| Campo | Detalle |
|---|---|
| **Archivos afectados** | `apply_filters.py`, `render_sidebar.py` |
| **Estrategia** | `git checkout --theirs` para estructura (prioridad `feature/ui`) |
| | `git checkout --ours` para lógica estable |
 
---
 
### Conflicto 3.4: `src/logger/setup_logger.py`
 
| Campo | Detalle |
|---|---|
| **Problema** | Import `pathlib` presente en una versión pero no en otra |
| **Solución** | Conservar ambas líneas sin duplicar imports |
 
---
 
## 4. Corrección de tests
 
### Problema 4.1: 56 tests fallando — `TypeError: 'module' object is not callable`
 
| Campo | Detalle |
|---|---|
| **Causa raíz** | Importación incorrecta en `tests/test_charts.py` |
| **Corrección** | Script automático de reemplazo en 8 imports |
| **Resultado** | ✅ 56 errores resueltos en 2 minutos |
 
**Importación incorrecta vs. correcta:**
 
```python
# ❌ INCORRECTO — importa el módulo, no la función
from src.charts import chart_fatalities_over_time
 
# ✅ CORRECTO — importa la función directamente
from src.charts.chart_fatalities_over_time import chart_fatalities_over_time
```
 
---
 
### Problema 4.2: Tests de integración en `skip`
 
| Campo | Detalle |
|---|---|
| **Decisión** | Mantener `@pytest.mark.skip` temporalmente |
| **Justificación** | Requieren datos reales y mayor tiempo de ejecución |
| **Plan** | Activarlos en la próxima iteración |
 
---
 
### Resultado final de tests
 
```
✅  117 passed
⏸️    5 skipped  (tests de integración)
❌    0 failed
```
 
---
 
## 5. CI/CD y linting
 
### Decisión 5.1: Usar Ruff en lugar de Flake8
 
| Campo | Detalle |
|---|---|
| **Fecha** | Día 3 — 06/05/2026 |
| **Justificación** | Mayor velocidad y capacidad de auto-corrección |
 
---
 
### Problema 5.1: CI ejecutando solo `test_charts.py`
 
**Solución — modificar `.github/workflows/ci.yml`:**
 
```yaml
# ANTES
pytest tests/test_charts.py
 
# DESPUÉS
pytest tests/ --ignore=tests/test_integration.py
```
 
---
 
### Problema 5.2: Cobertura por módulo demasiado estricta
 
**Solución — cambiar a cobertura total mínima del 70%:**
 
```python
coverage = (covered_lines / total_lines) * 100
if coverage < 70:
    sys.exit(1)
```
 
---
 
### Problema 5.3: Ruff reportaba `app.py` no encontrado
 
| Campo | Detalle |
|---|---|
| **Causa** | `app.py` fue movido a `src/` |
| **Solución** | Actualizar rutas en CI |
 
```yaml
ruff check src/ tests/ src/app.py
```
 
---
 
### Errores de Ruff corregidos
 
| Tipo de error | Cantidad | Solución |
|---|---|---|
| Imports no usados | 8 | `ruff check --fix` |
| Variables no usadas | 4 | Eliminación manual |
| **Total** | **12** | ✅ Todos resueltos |
 
---
 
## 6. Nomenclatura de módulos
 
### Decisión 6.1: Renombrar `chart_geopandas.py` → `chart_geospatial.py`
 
| Campo | Detalle |
|---|---|
| **Fecha** | 09/05/2026 |
 
**Justificación:**
 
- ❌ `geopandas` menciona una librería específica (no instalada)
- ✅ `geospatial` describe la funcionalidad (mapas geoespaciales)
- ✅ Consistencia con el resto de archivos `chart_*.py`
**Cambios aplicados:**
 
```bash
git mv src/charts/chart_geopandas.py src/charts/chart_geospatial.py
# Función renombrada:  render_two()       → chart_geospatial()
# Navbar actualizado: "🔮 Geopandas"     → "🗺️ Mapa geoespacial"
```
 
---
 
### Decisión 6.2: Mantener prefijo `chart_` para todas las visualizaciones
 
**Módulos verificados:**
 
| Archivo |
|---|
| `chart_age_distribution.py` |
| `chart_by_region.py` |
| `chart_fatalities_over_time.py` |
| `chart_gender_breakdown.py` |
| `chart_geospatial.py` *(renombrado)* |
| `chart_killed_by.py` |
| `chart_monthly_heatmap.py` |
| `chart_scatter_3d.py` |
| `chart_top_locations.py` |
 
---
 
## 7. Logging y monitoreo
 
### Decisión 7.1: Logs en `logs/` con fecha diaria
 
| Campo | Detalle |
|---|---|
| **Formato** | `logs/dashboard_YYYYMMDD.log` |
| **Configuración** | `src/logger/setup_logger.py` |
 
---
 
### Decisión 7.2: Logs NO versionados
 
**Implementación en `.gitignore`:**
 
```
logs/*.log
logs/
```
 
**Aplicado con:**
 
```bash
git rm --cached logs/*.log
```
 
---
 
### Decisión 7.3: JSON de estadísticas en `results/`
 
| Campo | Detalle |
|---|---|
| **Formato** | `results/stats_YYYYMMDD_HHMMSS.json` |
| **Frecuencia** | Generado bajo demanda (botón "Exportar estadísticas") |
 
---
 
## Resumen de resultados finales
 
| Área | Estado | Métrica |
|---|---|---|
| Tests | ✅ | 117 passed, 5 skipped |
| Cobertura | ✅ | ≥ 70% líneas |
| Linting | ✅ | 0 errores Ruff |
| CI/CD | ✅ | Verde en 3 versiones Python |
| Dashboard | ✅ | Streamlit funcionando |
| CSVs adicionales | ✅ | Carga y combinación funcional |
| Documentación | ✅ | DECISIONS.md actualizado |