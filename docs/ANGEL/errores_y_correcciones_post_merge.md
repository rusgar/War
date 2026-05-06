# Documentación de Errores y Correcciones post-Merge

**Fecha:** 06/05/2026

## Contexto

Durante el merge de las 3 ramas (`main`, `feature/visualizacion`, `pipeline`) se perdieron funciones del módulo logger y hubo conflictos en las llamadas a funciones.

---

## Errores Encontrados

### 1. Función `get_chart_logger` no existía

**Síntoma:**
```
ImportError: cannot import name 'get_chart_logger' from 'src.logger' (unknown location)
```

**Causa:** 
- El archivo original `src/logger.py` fue modularizado en directorio `src/logger/` 
- Se crearon archivos separados: `log_chart_rendered.py`, `log_data_loaded.py`, `log_filter_applied.py`, `setup_logger.py`
- La función `get_chart_logger` nunca fue creada en los nuevos archivos

**Ubicación:** `src/charts.py:33` intentaba importar `get_chart_logger`

---

### 2. Falta `__init__.py` en `src/logger/`

**Síntoma:**
```
ImportError: cannot import name 'get_chart_logger' from 'src.logger'
```

**Causa:** No existía archivo `src/logger/__init__.py` para exportar las funciones del paquete

---

### 3. Firma de `log_chart_rendered()` incorrecta

**Síntoma:**
```
TypeError: log_chart_rendered() takes 3 positional arguments but 4 were given
```

**Causa:** 
- La función original aceptaba 3 parámetros: `(log, chart_name, rows)`
- Pero en várias partes de `charts.py` se llamaba con 4 parámetros incluyendo `rows_rendered`
- Ejemplo en `src/charts.py:101`:
  ```python
  log_chart_rendered(chart_log, "chart_fatalities_over_time", len(df), 100)
  ```

---

### 4. Variable `log` no definida en `chart_age_distribution`

**Síntoma:**
```
NameError: name 'log' is not defined
```

**Causa:** En la función `chart_age_distribution` faltaba inicializar el logger

**Ubicación:** `src/charts.py:261`

---

## Correcciones Aplicadas

### 1. Crear función `get_chart_logger`

**Archivo:** `src/logger/log_chart_rendered.py`

Se agregó la función:
```python
def get_chart_logger(name: str = "charts") -> logging.Logger:
    """Crea y devuelve un logger específico para gráficos."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
```

---

### 2. Crear `__init__.py` 

**Archivo:** `src/logger/__init__.py`

```python
from src.logger.setup_logger import setup_logger
from src.logger.log_data_loaded import log_data_loaded
from src.logger.log_filter_applied import log_filter_applied
from src.logger.log_chart_rendered import log_chart_rendered, get_chart_logger
```

---

### 3. Corregir firma de `log_chart_rendered`

**Archivo:** `src/logger/log_chart_rendered.py`

Se agregó parámetro opcional:
```python
def log_chart_rendered(log: logging.Logger, chart_name: str, rows: int, rows_rendered: int = None) -> None:
    """Registra el renderizado de gráficos (nivel DEBUG)."""
    if rows_rendered is not None:
        log.debug("CHART_RENDERED | chart=%s | rows_used=%d | rows_rendered=%d", chart_name, rows, rows_rendered)
    else:
        log.debug("CHART_RENDERED | chart=%s | rows_used=%d", chart_name, rows)
```

---

### 4. Inicializar `log` en `chart_age_distribution`

**Archivo:** `src/charts.py`

Se agregó al inicio de la función:
```python
log = get_chart_logger("chart_age_distribution")
```

---

## Archivos Modificados

| Archivo | Acción |
|---------|--------|
| `src/logger/log_chart_rendered.py` | Agregado `get_chart_logger`, corregido firma de función |
| `src/logger/__init__.py` | Creado nuevo |
| `src/charts.py` | Agregado inicialización de `log` en `chart_age_distribution` |

---

## Lessons Learned

1. ** Modularización incompleta:** Cuando se divide un módulo, hay que crear el `__init__.py` y mantener todas las funciones que se usaban anteriormente.

2. **Firmas de funciones:** Cualquier cambio en firmas de funciones debe actualizarse en todos los lugares donde se usan.

3. **Merge de ramas:** Revisar que todas las funciones exportadas existan después de integrar ramas.