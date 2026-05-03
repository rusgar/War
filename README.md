# War Analytics Dashboard — CrisisScope Analytics

> **Dataset:** B'Tselem · 11.124 registros · conflicto israelí-palestino · 2000–2023  
> **Stack:** Python · Streamlit · Plotly · pytest · GitHub Actions  
> **Modalidad:** Pair programming · Live Share · 4 alumnos · 3 ramas · 4 días

---

## Lo que encontráis en este repo

Todo está en la raíz, sin estructura de carpetas. **La app funciona.** Ejecutad esto antes de tocar nada:

```bash
git clone https://github.com/rusgar/War
cd War
python -m venv .venv && source .venv/bin/activate   # Mac/Linux
python -m venv .venv && .venv\Scripts\activate       # Windows
pip install -r requirements.txt
streamlit run app.py
```

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

---

## Rotación (decidirla entre todos el Día 1 — anotarla en `docs/DECISIONS.md`)

|       | `feature/pipeline` | `feature/visualization` | `feature/ui` | Reviewer |
|-------|-------------------|------------------------|-------------|----------|
| Día 1 | &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| Día 2 | &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| Día 3 | &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| Día 4 | &nbsp; | &nbsp; | &nbsp; | &nbsp; |

**Regla:** nadie repite rama dos días seguidos.

---

## Flujo de trabajo diario — LEED ESTO CADA MAÑANA

### Cada mañana (antes de escribir código)

```bash
# 1. Actualizar main — el profesor habrá integrado el trabajo del día anterior
git checkout main
git pull origin main

# 2. Crear o actualizar vuestra rama del día
git checkout -b feature/<vuestra-rama>        # Día 1 (rama nueva)
git checkout feature/<vuestra-rama>           # Días 2, 3, 4 (rama existente)
git rebase origin/main                        # Traer los cambios integrados del profesor
```

### Durante el día (pair programming con Live Share)

1. El que comparte pantalla es el **Driver** — escribe el código
2. El otro es el **Navigator** — revisa, sugiere, busca docs
3. **Cambiad de rol cada 25 minutos** (técnica Pomodoro)
4. Committed semántico cada vez que una función está completa y sus tests pasan

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

## Estructura objetivo (propuesta — la decidís vosotros el Día 1)

Lo que **sí es obligatorio** al final:
- Toda la lógica en módulos dentro de `src/`
- Todos los tests en `tests/`
- `streamlit run app.py` funciona
- CI verde en las 4 versiones Python
- `docs/DECISIONS.md` relleno

Lo que decidís vosotros (y justificáis en `docs/DECISIONS.md`):
- Nombres exactos de carpetas y módulos
- Cómo dividís los módulos grandes
- Estrategia de imports

Propuesta orientativa:

```
War/
├── app.py                          ← punto de entrada (solo UI)
├── requirements.txt
├── .gitignore
├── fatalities.csv                  ← en .gitignore, no subir cambios
│
├── .github/
│   └── workflows/
│       └── ci.yml                  ← mover aquí el ci.yml de la raíz (Día 1)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py              ← solo: cargar y limpiar CSV
│   ├── logger.py                   ← solo: logging estructurado
│   ├── stats.py                    ← solo: estadísticas + exportar JSON
│   ├── charts.py                   ← solo: funciones puras df → Figure
│   ├── filters.py                  ← solo: apply_filters() pura
│   └── kpis.py                     ← solo: funciones _calc_*() puras
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
├── logs/                           ← generado por logger.py
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
- [ ] `feature/ui` → `app.py` arranca con los módulos de `src/`, sidebar visible
- [ ] **Reviewer** → CI configurado y verde en las 3 ramas, `test_integration.py` con los primeros tests
- [ ] **⏰ Antes de acabar:** push + mostrar al profesor

🔴 **Reto del profesor al final del Día 1** — se comunicará en clase

---

### Día 2 — Tests y estadísticas

**Objetivo:** cobertura ≥ 80% en cada módulo, `stats.py` exporta JSON, logs funcionan.

- [ ] `git pull origin main` y `git rebase origin/main` en cada rama
- [ ] `feature/pipeline` → `stats.py` completo, `logger.py` integrado, tests pasan
- [ ] `feature/visualization` → 6 gráficos implementados con logs de render
- [ ] `feature/ui` → KPIs con deltas, sidebar completo, `st.download_button`
- [ ] **Reviewer** → tests de integración: filtros + gráficos no rompen con datos vacíos
- [ ] **⏰ Antes de acabar:** push + mostrar al profesor

🔴 **Reto del profesor al final del Día 2** — se comunicará en clase

---

### Día 3 — Calidad y pipeline robusto

**Objetivo:** logs a fichero, JSON en `results/`, CI con matriz de 4 versiones Python.

- [ ] `git pull origin main` y `git rebase origin/main`
- [ ] `feature/pipeline` → logs a `logs/dashboard_YYYYMMDD.log`, exportar stats a `results/`
- [ ] `feature/visualization` → gráfico extra propuesto por el equipo, `chart_killed_by()`
- [ ] `feature/ui` → tabla explorable, descarga CSV filtrado, botón exportar JSON
- [ ] **Reviewer** → `docs/ARCHITECTURE.md` y `docs/Final.md` iniciados
- [ ] CI verde en 4 versiones Python (3.9, 3.10, 3.11, 3.12)
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

Si usaste IA para ese bloque: añade `[ai]` al final del mensaje.

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

---

## Comandos de referencia

```bash
# Setup inicial
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Tests de tu módulo con cobertura
pytest tests/test_<modulo>.py --cov=src/<modulo> --cov-report=term-missing -v

# Tests completos
pytest tests/ --cov=src --cov-report=term-missing -v

# App en local
streamlit run app.py

# Actualizar tu rama desde main cada mañana
git fetch origin
git rebase origin/main
```

---

## Criterios de evaluación

| Criterio | Peso |
|---|---|
| Dashboard funcional en demo (filtros + gráficos + KPIs) | 25% |
| Tests con cobertura ≥ 80% por módulo | 20% |
| Logs y JSON de estadísticas generados correctamente | 15% |
| Commits semánticos + `docs/*.md` actualizados | 15% |
| CI verde en las 4 versiones Python | 10% |
| Gestión de ramas: rotación, PRs, reviews diarios al profesor | 10% |
| Calidad del código (SRP, type hints, docstrings) | 5% |
