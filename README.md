# Conflict Fatalities Dashboard — Ejercicio 4 días

> **Dataset:** B'Tselem · 11.124 registros · 2000–2023  
> **Stack:** Python · Streamlit · Plotly · pytest · GitHub Actions  
> **Equipo:** 4 alumnos · 3 ramas · rotación diaria · releases en vivo del profesor

---

## Lo que tenéis en este repo (y nada más)

```
main/
├── fatalities.csv       ← el dataset, no subir cambios sobre él
├── README.md            ← este archivo
├── requirements.txt     ← dependencias fijas, no modificar
└── .gitignore           ← ya configurado
```

> El `ci.yml` lo encontráis en `requirements.txt` — tenéis que moverlo vosotros
> a `.github/workflows/ci.yml` como primera tarea del Día 1.

---

## Lo que tenéis que construir vosotros

Al final del Día 4 vuestro repo debe tener esta estructura:

```
conflict-dashboard/
├── fatalities.csv
├── README.md
├── requirements.txt
├── .gitignore
├── interface/
│   └── app.py   ← punto de entrada de Streamlit
│
├── .github/
│   └── workflows/
│       └── ci.yml                ← mover aquí el ci.yml del repo
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py            ← carga y limpieza del CSV
│   ├── logger.py                 ← logging estructurado
│   ├── stats.py                  ← estadísticas descriptivas + exportación JSON
│   ├── charts.py                 ← todos los gráficos Plotly
│   ├── filters.py                ← sidebar y lógica de filtrado
│   └── kpis.py                   ← métricas de cabecera
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_stats.py
│   ├── test_charts.py
│   ├── test_filters.py
│   ├── test_kpis.py
│   └── test_integration.py       ← tests entre módulos (rol reviewer)
│
├── docs/
│   ├── DECISIONS.md              ← decisiones de arquitectura del equipo
│   ├── ARCHITECTURE.md
│   └── <modulo>.md               ← uno por módulo implementado
│
├── logs/
│   └── dashboard_YYYYMMDD.log    ← generado automáticamente por logger.py
│
└── results/
    └── stats_YYYYMMDD_HHMMSS.json  ← generado por stats.py
```

**Importante:** la estructura de carpetas la decidís vosotros en equipo el Día 1.
La de arriba es una propuesta, no es obligatoria. Lo que sí es obligatorio:
- Todo el código en módulos dentro de una carpeta `src/`
- Todos los tests en una carpeta `tests/`
- La app arranca con `streamlit run app.py`(acordaros de estar en interface/)
- La pipeline CI pasa en verde

---

## Las 3 ramas — quién hace qué

| Rama | Módulos a crear | Responsabilidad |
|---|---|---|
| `feature/pipeline` | `data_loader.py` · `logger.py` · `stats.py` | Carga, limpieza, logging, estadísticas exportables |
| `feature/visualization` | `charts.py` | Todos los gráficos Plotly (mínimo 6) |
| `feature/ui` | `filters.py` · `kpis.py` · `app.py` | Sidebar, KPIs, layout, descarga de datos |

**4 alumnos, 3 ramas → siempre hay un Reviewer.**  
El Reviewer no tiene rama asignada ese día: revisa PRs, escribe `test_integration.py` y actualiza `docs/`.

---

## Rotación (decidirla el Día 1 y anotarla en DECISIONS.md)

|       | pipeline | visualization | ui | reviewer |
|-------|----------|---------------|----|----------|
| Día 1 |          |               |    |          |
| Día 2 |          |               |    |          |
| Día 3 |          |               |    |          |
| Día 4 |          |               |    |          |

Regla: nadie repite rama dos días seguidos.

---

## Plan de 4 días

### Día 1 — Estructura y pipeline base

- [ ] Decidir estructura de carpetas en equipo → documentar en `docs/DECISIONS.md`
- [ ] Mover `ci.yml` a `.github/workflows/ci.yml`
- [ ] Crear las 3 ramas, primer commit semántico en cada una
- [ ] `feature/pipeline`: `data_loader.py` carga el CSV, tests pasan
- [ ] `feature/visualization`: al menos 1 gráfico real implementado
- [ ] `feature/ui`: `app.py` arranca con placeholders, sidebar visible
- [ ] **Reviewer**: verifica que la CI está verde en las 3 ramas
- [ ] PR al final del día → merge solo si CI verde + 1 review aprobado

🔴 **Release del profesor al final del Día 1** — se añade un requisito nuevo al dataset o al filtrado. Tendréis que adaptar código y hacer PR.

---

### Día 2 — Visualizaciones y estadísticas

- [ ] Cada uno actualiza su rama desde `main` (`git rebase origin/main`)
- [ ] `feature/pipeline`: `stats.py` con estadísticas exportables a JSON
- [ ] `feature/visualization`: los 6 gráficos implementados
- [ ] `feature/ui`: KPIs con deltas, sidebar completo, `st.download_button`
- [ ] **Reviewer**: `test_integration.py` — filtros + gráficos no rompen con datos vacíos
- [ ] Cobertura de tests ≥ 80% en cada módulo propio

🔴 **Release del profesor al final del Día 2** — cambio en la firma de una función. Romperá algo intencionadamente.

---

### Día 3 — Calidad, logs y pipeline robusto

- [ ] `feature/pipeline`: logs a fichero (`logs/dashboard_YYYYMMDD.log`)
- [ ] `feature/visualization`: gráfico extra propuesto por el equipo
- [ ] `feature/ui`: tabla explorable, descarga CSV filtrado
- [ ] **Reviewer**: documentación completa en `docs/*.md`
- [ ] Todos los tests pasan, cobertura ≥ 80%

🔴 **Release del profesor al final del Día 3** — refactor de interfaz: una función cambia de módulo. Actualizad imports sin romper tests.

---

### Día 4 — Integración final y demo

- [ ] Feature freeze a las 10:00 — solo bugfixes
- [ ] Merge final a `main` — PR del equipo completo
- [ ] `results/` con el JSON de estadísticas del dataset real
- [ ] Demo en vivo: cada alumno explica su rama y decisiones

---

## Qué debe mostrar el dashboard

1. **KPIs** — total fatalidades, edad media, % menores, años cubiertos, regiones
2. **Líneas temporales** — fatalidades por año y ciudadanía
3. **Heatmap mensual** — mes × año
4. **Histograma de edades** — por ciudadanía
5. **Sunburst** — ciudadanía → género
6. **Barras horizontales** — por región
7. **Treemap** — región → distrito → localización
8. **Sidebar con filtros** — años, ciudadanía, género, región, killed_by
9. **Tabla explorable** con descarga CSV
10. **Botón exportar estadísticas** → JSON en `results/`

---

## Reglas de commits semánticos

```
feat(data_loader):  nueva funcionalidad
fix(filters):       corrección de bug
test(charts):       añadir o modificar tests
docs(pipeline):     documentación
refactor(kpis):     refactor sin cambio de comportamiento
ci:                 cambios en pipeline
```

---

## Reglas de uso de IA

Podéis usar Claude, OpenCode, Gemini, Arena o cualquier otra IA:

✅ Permitido: pedir explicaciones, sugerencias de mejora, datos de prueba, nombres de variables  
✅ Permitido: generar código y adaptarlo después de entenderlo  
❌ No permitido: copy-paste sin leer ni ejecutar localmente  
❌ No permitido: que la IA escriba los mensajes de commit  
❌ No permitido: subir tests generados por IA sin haberlos revisado

> Si en la demo no puedes explicar una línea de tu código, no debería estar en tu rama.

---

## 1 Comandos de referencia

```bash
# Setup
python -m venv .venv && source .venv/bin/activate   # Mac/Linux
python -m venv .venv && .venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Crear tu rama
git checkout main && git pull origin main
git checkout -b feature/<tu-rama>

# Actualizar rama desde main cada mañana
git fetch origin && git rebase origin/main

# Actualizar requirements.txt con tus nuevas dependencias
pip freeze > requirements.txt

# Instalar una librería específica y actualizar requirements
pip install plotly pandas && pip freeze > requirements.txt

# Verificar dependencias desactualizadas
pip list --outdated

# Tests de tu módulo con cobertura
pytest tests/test_<modulo>.py --cov=src/<modulo> --cov-report=term-missing -v

# App en local
streamlit run app.py
```
---

## 2 Control de versiones avanzado

```bash
# Ver estado y cambios antes de commitear
git status
git diff

# Commit con mensaje descriptivo
git add .
git commit -m "feat: descripción clara del cambio"

# Subir rama remota por primera vez
git push -u origin feature/<tu-rama>

# Subir cambios subsecuentes
git push

# Ver historial de commits
git log --oneline --graph --all
```

---

## 3 Resolución de conflictos (importante)

```bash
# Si rebase falla, abortar y empezar de nuevo
git rebase --abort

# Alternativa: merge en lugar de rebase (más seguro)
git merge origin/main

# Ver conflictos pendientes
git diff --name-only --diff-filter=U

# Después de resolver conflictos manualmente
git add .
git rebase --continue   # si usaste rebase
# o
git commit -m "merge: resolver conflictos"  # si usaste merge

```

---


##  4 Testing y debugging

```bash
# Tests con verbose y stop on first failure
pytest tests/test_<modulo>.py -v -x

# Tests de un test específico
pytest tests/test_<modulo>.py::test_nombre_funcion -v

# Tests con cobertura y reporte HTML
pytest tests/test_<modulo>.py --cov=src/<modulo> --cov-report=html
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows

# Debug mode en Streamlit
streamlit run app.py --logger.level=debug

```

---


## 🗃️ Descripción del Dataset

| Columna | Descripción |
|---|---|
| `name` | Nombre de la víctima |
| `date_of_event` | Fecha del incidente |
| `age` | Edad |
| `citizenship` | Palestinian / Israeli / Foreign |
| `event_location_region` | Región del incidente (West Bank, Gaza Strip, Israel...) |
| `event_location_district` | Distrito |
| `gender` | M / F |
| `type_of_injury` | gunfire / explosion / stabbing... |
| `ammunition` | live ammunition / missile / bomb... |
| `killed_by` | Israeli security forces / Palestinian civilians / Israeli civilians... |
| `took_part_in_the_hostilities` | Yes / No / Unknown |

---


## Criterios de evaluación

| Criterio | Peso |
|---|---|
| Dashboard funcional en demo (filtros + gráficos + KPIs) | 25% |
| Tests con cobertura ≥ 80% por módulo | 20% |
| Logs y JSON de estadísticas generados correctamente | 15% |
| Commits semánticos + `docs/*.md` actualizados | 15% |
| CI verde en todas las ramas durante los 4 días | 10% |
| Gestión del equipo: rotación, PRs, reviews | 10% |
| Calidad del código (funciones puras, sin duplicación) | 5% |