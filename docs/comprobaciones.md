# Comandos para comprobar:

## 1. Ver el estado actual de main:

````
git checkout main
git log --oneline -5

````
## 2. Ver si main ha cambiado (vs el remoto):

````
git fetch origin
git status
 ````
###  Resultado obtenido:
- main sincronizado con origin/main
- Sin cambios no deseados
- Los alumnos trabajan en sus ramas sin afectar main
 ###  Para integrar ramas de alumnos:
git merge origin/nombre-rama-alumno

 ---
# Integracion
## Opción 1: Integrar una por una

````
# Pipeline
git merge origin/pipeline

# Visualización
git merge origin/feature/visualizacion

# UI
git merge origin/feature/ui
````
## Conflictos

Conflictos a resolver:
---
- docs/DECISIONS.md - ambos modificaron

- logs/dashboard_20260505.log - ambos añadieron (archivo de log)

- src/logger/setup_logger.py - ambos modificaron
---

### Aceptamos cambios
````

git checkout --ours docs/DECISIONS.md
git checkout --ours logs/dashboard_20260505.log
git checkout --ours src/logger/setup_logger.py
git add docs/DECISIONS.md logs/dashboard_20260505.log src/logger/setup_logger.py
git commit -m "Merge feature/ui - resuelto conflictos aceptando cambios de UI"
````

## Continuacion, después de que tú integres sus ramas a main:

````

git checkout main
git merge origin/pipeline
git merge origin/feature/visualizacion  
git merge origin/feature/ui
git push origin main
````