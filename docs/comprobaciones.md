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

### Resolucion
    - Your branch is up to date with 'origin/main'.

- nothing to commit, working tree clean
- a1086f8 (HEAD -> main, origin/main, origin/HEAD) Actualizar comprobaciones.md con resolución de conflictos
- 8ef2377 Merge feature/ui - resuelto conflictos aceptando cambios de UI
7- eb176e Merge remote-tracking branch 'origin/pipeline' merge de la rama pipeline a origen con fecha 05052026 :wq
- 25d41be Añadir documentación de comprobación de main
- 1f3fff7 (origin/pipeline) LOGS

## Programadores
**Cada alumno en su rama debe:**
````

git checkout su-rama
git merge main
git push origin su-rama

````

# Mensaje para vosotros:
"He integrado todas vuestras ramas en main como solicitasteis. Sin embargo, al probar la aplicación, hay errores de importación porque cada uno trabajó por separado y no coordinasteis la interfaz entre módulos.

### Vuestra tarea ahora es:

- Actualizar vuestra rama local con git merge main

- Resolver los errores de importación en vuestros archivos

- Asegurar que la aplicación funciona correctamente

- Subir las correcciones a vuestras ramas

- Esto es parte normal del trabajo colaborativo con Git."

Fecha de última actualización: 05/05/2026

---
---


# 📢 Actualización para alumnos: Sincronizar vuestras ramas

**⚠️ IMPORTANTE:** Ejecutad estos comandos HOY para tener los últimos cambios (`.gitignore` actualizado, limpieza de logs, etc.)

## 🔧 Comandos según vuestra rama

### Si trabajáis en `feature/visualizacion`:
```bash
git checkout feature/visualizacion
git pull origin feature/visualizacion --rebase

### Si trabajáis en feature/ui:

git checkout feature/ui
git pull origin feature/ui --rebase

### Si trabajáis en pipeline:

git checkout pipeline
git pull origin pipeline --rebase

```

## Qué veréis durante el proceso
- Antes de ejecutar los comandos:
git status
### Veréis: "Your branch is behind 'origin/...' by X commits"

## Después del git pull:
✅ Archivo .gitignore actualizado (ignora logs)

✅ Limpieza de archivos .log del repositorio

✅ Últimos cambios integrados desde integration

Fecha de última actualización: 06/05/2026