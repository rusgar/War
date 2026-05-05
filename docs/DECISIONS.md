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
| 3   | | | | |
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


