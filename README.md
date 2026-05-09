# War Analytics Dashboard — CrisisScope Analytics

> **Dataset:** B'Tselem · 11.124 registros · conflicto israelí-palestino · 2000–2023  
> **Stack:** Python · Streamlit · Plotly · pandas · pytest · Ruff · GitHub Actions  
> **Modalidad:** Pair programming · Live Share · 4 alumnos · 3 ramas · 4 días

![Python](https://img.shields.io/badge/Python-3.9%20|%203.10%20|%203.11%20|%203.12-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat&logo=plotly&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?style=flat&logo=pandas&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-passing-009688?style=flat&logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-linting-D7FF64?style=flat&logo=ruff&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=flat&logo=githubactions&logoColor=white)

---

## Equipo

| Alumno | GitHub |
|---|---|
| Ángel | [@kindred-98](https://github.com/kindred-98) |
| Andrés | [@zombiradiactivo](https://github.com/zombiradiactivo) |
| Carlos Barrientos | [@carlosbarrientosarias27-star](https://github.com/carlosbarrientosarias27-star) |
| Israel | [@israelscr-prog](https://github.com/israelscr-prog) |
| Javier | [@yioqse](https://github.com/yioqse) |


---

## Lo que encontráis en este repo

El proyecto está estructurado en módulos dentro de `src/`. **La app funciona.** Ejecutad esto antes de tocar nada:

```bash
git clone https://github.com/rusgar/War
cd War
python -m venv .venv && source .venv/bin/activate   # Mac/Linux
python -m venv .venv && .venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Lanzar el dashboard
python main.py
```

> `main.py` es el lanzador — arranca `src/app.py` sin necesidad de invocar Streamlit directamente.

Si el dashboard abre en el navegador, estáis listos. Ahora viene vuestro trabajo.

---

## El problema

El código funciona, pero viola todos los principios de ingeniería de software:

| Archivo | Problema |
|---|---|
| `app.py` | Mezcla UI, lógica de negocio y llamadas a todos los módulos |
| `data_loader.py` | Mezcla carga de CSV, limpieza, logging y estadísticas |
| `charts.py` | Sin type hints, sin docstrings, sin tests |
| `filters.py` | La UI del sidebar y la lógica de filtrado en la misma función |
| `kpis.py` | Los cálculos viven dentro de las funciones de render |
| `logger.py` | Existe pero no está integrado en ningún módulo |
| `stats.py` | Existe pero nadie lo llama ni lo testea |
| `test_*.py` | Existen pero tienen todos los tests en `pytest.skip` |
| `ci.yml` | Pipeline incompleto, en la raíz en vez de en `.github/workflows/` |

**Vuestra misión:** modularizar, estructurar, testar, integrar el logging, completar el CI y dejar el proyecto en estado profesional.

---

## Las 3 ramas — quién hace qué cada día

| Rama | Responsabilidad | Módulos principales |
|---|---|---|
| `feature/pipeline` | Carga de datos, limpieza, logging, estadísticas | `data_loader.py`, `logger.py`, `stats.py` |
| `feature/visualization` | Todos los gráficos Plotly | `charts.py` |
| `feature/ui` | Sidebar, KPIs, layout de la app | `filters.py`, `kpis.py`, `app.py` |

**4 alumnos, 3 ramas → siempre hay un Reviewer.**  
El Reviewer no tiene rama ese día: revisa PRs, completa `test_integration.py` y actualiza `docs/`.

### Creación de la rama de integración

```bash
git checkout -b integration
```

---

## Rotación (decidirla entre todos el Día 1 — anotarla en `docs/DECISIONS.md`)

| | `feature/pipeline` | `feature/visualization` | `feature/ui` | Reviewer |
|---|---|---|---|---|
| Día 1 | Carlos | &nbsp; | &nbsp; | &nbsp; |
| Día 2 | Andrés y Carlos | Angel | Israel | &nbsp; |
| Día 3 | &nbsp; | Israel y Carlos | Andrés y Angel | &nbsp; |
| Día 4 | &nbsp; | Andres y Israel|Angel y Andrés| &nbsp; |

**Regla:** nadie repite rama dos días seguidos (a no ser por ayudar).

---

## Flujo de trabajo diario — LEED ESTO CADA MAÑANA

### Cada mañana (antes de escribir código)

```bash
# 1. Actualizar main — el profesor habrá integrado el trabajo del día anterior
git checkout integration
git pull origin integration

# 2. Crear o actualizar vuestra rama del día
git checkout -b feature/<vuestra-rama>   # Día 1 (rama nueva)
git checkout feature/<vuestra-rama>      # Días 2, 3, 4 (rama existente)
git rebase origin/integration            # Traer los cambios integrados del profesor
```

### Durante el día (pair programming con Live Share)

1. El que comparte pantalla es el **Driver** — escribe el código
2. El otro es el **Navigator** — revisa, sugiere, busca docs
3. **Cambiad de rol cada 25 minutos** (técnica Pomodoro)
4. Commit semántico cada vez que una función está completa y sus tests pasan

```bash
# Ciclo de trabajo por función

# 1. Implementar la función
# 2. Ejecutar sus tests
pytest tests/test_<modulo>.py -v --cov=src/<modulo> --cov-report=term-missing

# 3. Si pasa → commit semántico
git add src/<modulo>.py tests/test_<modulo>.py
git commit -m "feat(filters): implement apply_filters with year range"

# 4. Push
git push origin feature/<vuestra-rama>
```

### Antes de acabar el día (OBLIGATORIO)

```
⏰ 30 minutos antes del fin de la sesión:
   1. Aseguraos de que el CI está verde en vuestra rama
   2. Haced push de todo lo que tengáis
   3. Mostrádselo al profesor → él decide qué integra en main
   4. Si hay algo roto → es mejor un commit parcial documentado que nada
```

---

## Estructura del proyecto

```
War/
├── main.py                         ← lanzador (ejecuta src/app.py vía Streamlit)
├── requirements.txt
├── .gitignore
├── fatalities.csv                  ← en .gitignore, no subir cambios
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   ├── __init__.py
│   ├── app.py                      ← punto de entrada UI (solo UI)
│   ├── charts/                     ← 9 módulos de visualización Plotly
│   ├── data_loader/                ← carga y limpieza de CSV
│   ├── filters/                    ← lógica de filtros y sidebar
│   ├── kpis/                       ← cálculos económicos (KPIs)
│   ├── logger/                     ← logging estructurado
│   ├── pages/                      ← 7 módulos UI modulares
│   └── stats/                      ← estadísticas y exportación JSON
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_stats.py
│   ├── test_charts.py
│   ├── test_filters.py
│   ├── test_kpis.py
│   └── test_integration.py
│
├── docs/
│   ├── DECISIONS.md                ← rellenar el Día 1 antes de codificar
│   ├── ARCHITECTURE.md
│   └── Final.md
│
├── logs/                           ← generado por logger (no versionado)
└── results/                        ← generado por stats.py
```

---

## Plan de 4 días

### Día 1 — Estructura y arranque

**Objetivo:** el proyecto tiene estructura de carpetas, la CI funciona, cada rama tiene al menos una función implementada y testeada.

- [ ] Decidir estructura en equipo (15 min) → `docs/DECISIONS.md`
- [ ] Mover `ci.yml` a `.github/workflows/`
- [ ] Crear las 3 ramas, primer commit semántico en cada una
- [ ] `feature/pipeline` → `data_loader.py` en `src/`, limpio, con tests que pasan
- [ ] `feature/visualization` → al menos 2 gráficos implementados y testeados
- [ ] `feature/ui` → `src/app.py` arranca con los módulos de `src/`, sidebar visible
- [ ] **Reviewer** → CI configurado y verde en las 3 ramas, `test_integration.py` con los primeros tests
- [ ] **⏰ Antes de acabar:** push + mostrar al profesor

🔴 **Reto del profesor al final del Día 1** — se comunicará en clase

---

### Día 2 — Tests y estadísticas

**Objetivo:** cobertura ≥ 70% total, `stats.py` exporta JSON, logs funcionan.

- [ ] `git pull origin main` y `git rebase origin/main` en cada rama
- [ ] `feature/pipeline` → `stats.py` completo, `logger.py` integrado, tests pasan
- [ ] `feature/visualization` → 6 gráficos implementados con logs de render
- [ ] `feature/ui` → KPIs con deltas, sidebar completo, `st.download_button`
- [ ] **Reviewer** → tests de integración: filtros + gráficos no rompen con datos vacíos
- [ ] **⏰ Antes de acabar:** push + mostrar al profesor

🔴 **Reto del profesor al final del Día 2** — se comunicará en clase

---

### Día 3 — Calidad y pipeline robusto

**Objetivo:** logs a fichero, JSON en `results/`, CI con matriz de versiones Python.

- [ ] `git pull origin main` y `git rebase origin/main`
- [ ] `feature/pipeline` → logs a `logs/dashboard_YYYYMMDD.log`, exportar stats a `results/`
- [ ] `feature/visualization` → gráfico extra propuesto por el equipo, `chart_killed_by()`
- [ ] `feature/ui` → tabla explorable, descarga CSV filtrado, botón exportar JSON
- [ ] **Reviewer** → `docs/ARCHITECTURE.md` y `docs/Final.md` iniciados
- [ ] CI verde en 3 versiones Python (3.10, 3.11, 3.12)
- [ ] **⏰ Antes de acabar:** push + mostrar al profesor

🔴 **Reto del profesor al final del Día 3** — se comunicará en clase

---

### Día 4 — Integración final y demo

**Objetivo:** `main` con todo integrado, dashboard funcional, demo en vivo.

- [ ] `git pull origin main` y `git rebase origin/main`
- [ ] Feature freeze a las 10:00 → solo bugfixes
- [ ] `docs/Final.md` completado con inventario de uso de IA
- [ ] `results/` con el JSON de estadísticas generado del dataset real
- [ ] **Demo en vivo:** cada alumno explica su rama y las decisiones tomadas
- [ ] El profesor hace el merge final a `main`

---

## Comandos de referencia

```bash
# Setup inicial
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Lanzar la app
python main.py

# Tests de tu módulo con cobertura
pytest tests/test_<modulo>.py --cov=src/<modulo> --cov-report=term-missing -v

# Tests completos (excluyendo integración)
pytest tests/ --ignore=tests/test_integration.py --cov=src --cov-report=term-missing -v

# Linting con Ruff
ruff check src/ tests/

# Linting con auto-corrección
ruff check src/ tests/ --fix

# Actualizar tu rama desde main cada mañana
git fetch origin
git rebase origin/main
```

---

## Reglas de commits semánticos

```
feat(data_loader):   nueva funcionalidad
fix(filters):        corrección de bug
test(charts):        añadir o modificar tests
docs(pipeline):      documentación
refactor(kpis):      refactor sin cambio de comportamiento
ci:                  cambios en el pipeline
chore:               tareas de mantenimiento (mover archivos, etc.)
```

Si usaste IA para ese bloque, añade `[ai]` al final del mensaje:

```bash
feat(filters): implement apply_filters with year range [ai]
test(kpis): add _calc_pct_minors unit tests
docs(decisions): complete day 1 architecture decisions
ci: move ci.yml to .github/workflows with python matrix
```

---

## Reglas de uso de IA

Podéis usar Claude, OpenCode, Gemini, Arena o cualquier otra IA:

✅ Pedir que identifique violaciones del SRP  
✅ Generar esqueleto de docstrings y completar los ejemplos vosotros  
✅ Generar casos base de tests y añadir edge cases propios  
✅ Pedir que explique el código que generó  
❌ Copy-paste sin leer ni ejecutar localmente  
❌ Que la IA escriba los mensajes de commit  
❌ Subir tests sin verificar que pasan en verde  
❌ No poder explicar una línea de vuestro código en la demo

> **Si en la demo no puedes explicar una línea de tu código, no debería estar en tu rama.**