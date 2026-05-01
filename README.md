# Conflict Fatalities Dashboard — Ejercicio 4 días

> **Dataset:** B'Tselem · 11.124 registros · 2000–2023  
> **Stack:** Python · Streamlit · Plotly · pytest · GitHub Actions  
> **Equipo:** 4 alumnos · 3 ramas · rotación diaria · releases en vivo

---

## Lo primero que tenéis que hacer (Día 1, hora 0)

Habéis recibido los archivos **totalmente planos**, sin estructura de carpetas.  
**Vuestra primera tarea es decidir en equipo cómo organizarlos** y crear la estructura del proyecto vosotros mismos antes de escribir una sola línea de código.

El repo de `main` solo tendrá esto al inicio:

```
fatalities.csv
README.md
requirements.txt
.gitignore
ci.yml           ← copiarlo a .github/workflows/
```

Todo lo demás lo construís vosotros.

---

## Las 3 ramas — quién hace qué

| Rama | Responsabilidad | Módulos principales |
|---|---|---|
| `feature/pipeline` | Carga de datos, limpieza, logging, estadísticas descriptivas | `data_loader.py`, `logger.py`, `stats.py` |
| `feature/visualization` | Todos los gráficos Plotly | `charts.py` |
| `feature/ui` | Sidebar, KPIs, layout de la app | `filters.py`, `kpis.py`, `app.py` |

> **4 alumnos, 3 ramas:** en cada sprint hay un alumno que no tiene rama asignada.  
> Ese alumno hace de **Reviewer**: revisa PRs, escribe tests de integración, actualiza docs.

---

## Rotación (la decide el equipo el Día 1)

Ejemplo de rotación posible — podéis cambiarla:

|          | pipeline | visualization | ui | reviewer |
|----------|----------|---------------|----|----------|
| **Día 1** | A | B | C | D |
| **Día 2** | D | A | B | C |
| **Día 3** | C | D | A | B |
| **Día 4** | B | C | D | A |

Regla: **nadie puede estar dos días seguidos en la misma rama.**  
El reviewer del día anterior tiene prioridad para elegir rama al día siguiente.

---

## Plan de 4 días

### Día 1 — Estructura y pipeline base

**Objetivo del día:** la app arranca, los datos cargan, el pipeline CI está verde.

- [ ] Decidir estructura de carpetas en equipo (15 min, documentar en `docs/DECISIONS.md`)
- [ ] Crear repo GitHub, proteger `main` (require PR + 1 review)
- [ ] Cada uno crea su rama y hace su primer commit semántico
- [ ] **feature/pipeline:** `data_loader.py` funciona, `logger.py` registra eventos, tests pasan
- [ ] **feature/ui:** `app.py` arranca con placeholders, `filters.py` skeleton con sidebar vacío
- [ ] **feature/visualization:** `charts.py` con al menos 1 gráfico real implementado
- [ ] **Reviewer:** configura CI (`ci.yml`), verifica que la pipeline pasa en todas las ramas
- [ ] PR al final del día → merge a `main` solo si CI verde + review aprobado

**🔴 Release del profesor al final del Día 1:**  
Se añadirá una nueva columna al CSV o un requisito nuevo de filtrado.  
Tendréis que adaptar `data_loader.py` y los filtros.

---

### Día 2 — Visualizaciones y estadísticas

**Objetivo del día:** dashboard funcional con mínimo 4 gráficos y KPIs visibles.

- [ ] Merge de los PRs del Día 1 → cada uno actualiza su rama desde `main`
- [ ] **feature/pipeline:** `stats.py` con estadísticas descriptivas exportables (CSV/JSON)
- [ ] **feature/visualization:** implementar los 6 gráficos, logs de renders
- [ ] **feature/ui:** KPIs con deltas, sidebar completo con todos los filtros
- [ ] **Reviewer:** tests de integración (filtros → gráficos no rompen con datos vacíos)
- [ ] Cobertura de tests ≥ 80% en cada módulo propio

**🔴 Release del profesor al final del Día 2:**  
Cambio en la firma de una función (ej. `load_data()` recibirá un parámetro nuevo).  
El cambio romperá algo intencionadamente. Tendréis que arreglarlo y hacer el PR.

---

### Día 3 — Calidad, logs y pipeline avanzado

**Objetivo del día:** logs estructurados, exportación de estadísticas, pipeline robusto.

- [ ] **feature/pipeline:** logs con `logging` estándar de Python (nivel INFO/WARNING/ERROR), exportar stats a `results/stats_YYYYMMDD.json`
- [ ] **feature/visualization:** gráfico adicional propuesto por el equipo (libre elección)
- [ ] **feature/ui:** tabla explorable con `st.dataframe`, descarga de datos filtrados con `st.download_button`
- [ ] **Reviewer:** documentación completa en `docs/*.md`, README actualizado
- [ ] Todos los tests pasan, cobertura ≥ 80%

**🔴 Release del profesor al final del Día 3:**  
Refactor de interfaz: una función cambia de módulo.  
Tendréis que actualizar imports en toda la app sin romper tests.

---

### Día 4 — Integración final y demo

**Objetivo del día:** app completa, presentación en vivo.

- [ ] Feature freeze a las 10:00 — solo bugfixes
- [ ] Merge final a `main` — PR del equipo completo
- [ ] `results/` con las estadísticas exportadas del dataset real
- [ ] Demo en vivo: cada alumno explica su rama y las decisiones tomadas
- [ ] **Reto extra:** añadir un gráfico de comparativa entre lo que generó la IA y lo que reescribisteis vosotros (git diff visual)

---

## Qué debe tener el repo al final

```
conflict-dashboard/
├── app.py
├── requirements.txt
├── .gitignore
├── fatalities.csv            ← no subir a git (.gitignore)
├── results/
│   └── stats_YYYYMMDD.json  ← generado por stats.py
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── logger.py
│   ├── stats.py
│   ├── charts.py
│   ├── filters.py
│   └── kpis.py
├── tests/
│   ├── test_data_loader.py
│   ├── test_stats.py
│   ├── test_charts.py
│   ├── test_filters.py
│   ├── test_kpis.py
│   └── test_integration.py   ← del reviewer
├── docs/
│   ├── DECISIONS.md          ← decisiones de arquitectura del equipo
│   ├── ARCHITECTURE.md
│   └── *.md por módulo
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Reglas de commits semánticos

```
feat(data_loader):  nueva funcionalidad
fix(filters):       corrección de bug
test(charts):       añadir o modificar tests
docs(pipeline):     documentación
refactor(kpis):     refactor sin cambio de comportamiento
ci:                 cambios en pipeline
chore:              tareas de mantenimiento
```

Ejemplos reales:
```
feat(data_loader): add age_group categorical column
fix(filters): handle empty dataframe in apply_filters
test(charts): add chart_by_region returns figure assertion
docs(pipeline): document logger module API
refactor(stats): extract _group_by_year to helper
ci: add per-branch coverage threshold check
```

---

## Reglas de uso de IA (importante)

Podéis usar Claude, OpenCode, Gemini, Arena o cualquier otra IA. Con estas normas:

1. **Todo código generado por IA debe ser revisado y entendido** antes del commit. Si no lo puedes explicar en la demo, no lo subas.
2. **Los tests los escribís vosotros**, no la IA. Los tests son vuestro contrato con el código.
3. **Los commits semánticos y los docs son vuestros**. La IA puede sugerir, pero el mensaje del commit lo escribe quien entiende el cambio.
4. **Está permitido** pedirle a la IA que explique código, sugiera mejoras, genere datos de prueba, proponga nombres de variables.
5. **No está permitido** hacer copy-paste de la IA sin leer, subir código que no compiláis localmente antes, ni usar la IA para los mensajes de commit.

---

## Comandos de referencia

```bash
# Setup inicial
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Tests con cobertura de tu módulo
pytest tests/test_<tumodulo>.py --cov=src/<tumodulo> --cov-report=term-missing -v

# Tests completos
pytest tests/ --cov=src --cov-report=term-missing -v

# App en local
streamlit run app.py

# Crear tu rama
git checkout main && git pull origin main
git checkout -b feature/<turама>

# Actualizar tu rama desde main (hacer esto cada mañana)
git fetch origin
git rebase origin/main
```

---

## Criterios de evaluación

| Criterio | Peso | Cómo se mide |
|---|---|---|
| Funcionalidad completa (app arranca, filtros y gráficos funcionan) | 25% | Demo en vivo |
| Tests con cobertura ≥ 80% por módulo | 20% | `pytest --cov` en CI |
| Logs y estadísticas exportadas correctamente | 15% | Revisar `results/` |
| Commits semánticos + docs actualizados | 15% | `git log --oneline` |
| CI verde en todas las ramas durante los 4 días | 10% | GitHub Actions |
| Gestión del equipo: rotación, PRs, reviews | 10% | Historial de PRs |
| Calidad del código (sin duplicación, funciones puras) | 5% | Code review final |
