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