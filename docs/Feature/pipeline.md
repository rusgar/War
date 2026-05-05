# Fase 1 - data_loader 

## 1. Modularización de la Limpieza (Funciones Internas)
Se han extraído las responsabilidades de limpieza en funciones especializadas:

_normalize_columns: Se encarga de estandarizar los nombres de las columnas.

Elimina espacios en blanco.

Convierte a minúsculas.

Sustituye espacios por guiones bajos (snake_case).

_apply_type_conversions: Gestiona la integridad de los tipos de datos.

Convierte date_of_event y date_of_death a objetos datetime.

Limpia y convierte la columna age a formato numérico.

Estandariza los valores de género (Male, Female, Unknown).

_add_derived_features: Genera nuevas columnas para facilitar el análisis posterior.

Crea las columnas year, month y month_name a partir de la fecha del evento.

Implementa age_group utilizando pd.cut para clasificar registros por rangos de edad (Minor, Young, Adult, etc.).

## 2. Mejoras en la Gestión de Rutas y Logging
Se actualizó la ruta por defecto a ./data/fatalities.csv para reflejar la estructura del proyecto.

Se integró el sistema de logging para informar sobre el inicio de la carga, el número de registros procesados y el estado final de las columnas.

## 3. Eliminación de Lógica Externa
Se eliminó la función de estadísticas descriptivas (get_summary_stats) de este módulo. Siguiendo el principio de responsabilidad única, esta lógica se ha trasladado al módulo especializado src/stats.py.

--- 

# Fase 2: Logger (`src/logger.py`)

Se ha implementado un sistema de registro centralizado que permite el seguimiento detallado de la ejecución de la aplicación, facilitando tanto la depuración en desarrollo como la auditoría en producción.

### 1. Configuración del Logger Principal (`setup_logger`)
La función `setup_logger` establece la infraestructura base para capturar eventos en la aplicación.

* **Handlers Duales**: Se han configurado dos manejadores de salida:
    * **StreamHandler**: Dirige los logs a la consola para visibilidad inmediata durante la ejecución.
    * **FileHandler**: Persiste los registros en archivos dentro del directorio `logs/`. Los archivos se nombran dinámicamente con la fecha actual (`dashboard_YYYYMMDD.log`).
* **Formato Estructurado**: Se utiliza un formato común (`LOG_FORMAT`) que incluye marca de tiempo, nivel de prioridad, nombre del módulo y el mensaje del evento.
* **Prevención de Duplicados**: Se incluyó una verificación de `logger.handlers` para asegurar que no se añadan múltiples handlers idénticos si la función se invoca repetidamente.

### 2. Helpers de Eventos Estructurados
Para estandarizar los mensajes en todo el pipeline, se crearon funciones de ayuda que generan entradas de log con un esquema consistente:

* **`log_data_loaded`**: Registra hitos de carga de datos, incluyendo la ruta del archivo y el número de filas procesadas.
    * *Formato*: `DATA_LOADED | rows=%d | path=%s`
* **`log_filter_applied`**: Informa sobre las operaciones de filtrado, detallando los criterios aplicados y el volumen de datos antes y después del filtro.
    * *Formato*: `FILTER_APPLIED | before=%d | after=%d | filters=%s`
* **`log_chart_rendered`**: Registra eventos de visualización en nivel `DEBUG`, indicando qué gráfico se generó y cuántos registros se utilizaron.
    * *Formato*: `CHART_RENDERED | chart=%s | rows_used=%d`

### 3. Gestión de Persistencia
* **Directorio Automático**: El módulo detecta la ausencia de la carpeta `logs/` y la crea automáticamente al iniciarse.
* **Codificación UTF-8**: Se garantiza que los archivos de log soporten caracteres especiales mediante la configuración explícita de la codificación en el `FileHandler`.

--- 

# Fase 3: Stats (`src/stats.py`)

Se ha desarrollado un módulo especializado para el cálculo de métricas descriptivas y la exportación de datos analíticos en formatos estructurados (JSON y DataFrames pivotados).

### 1. Motor de Cálculo Descriptivo (`compute_descriptive_stats`)
Se implementó una función robusta que genera un perfil completo del dataset actual (sea filtrado o completo).

* **Seguridad y Validación**: Se añadió una comprobación de entrada para manejar DataFrames vacíos, evitando errores en el cálculo de medias o porcentajes.
* **Métricas Temporales**: Cálculo dinámico del rango de fechas (`date_range`) con soporte para valores nulos (`NaT`) mediante conversión a formato ISO.
* **Análisis Demográfico**:
    * Estadísticas de edad detalladas (media, mediana, desviación estándar, mínimos y máximos).
    * Cálculo automático del porcentaje de menores de edad (`pct_minors`).
* **Distribuciones de Categoría**: Generación de diccionarios de frecuencia para ciudadanía, género, año del evento y región geográfica.

### 2. Agregaciones Avanzadas
Se incluyó la función `fatalities_by_year_citizenship` para facilitar análisis comparativos complejos.

* **Tablas Pivot**: Implementación de una tabla dinámica que cruza el año del evento con la ciudadanía de las víctimas.
* **Totales Calculados**: Se añadió automáticamente una columna de "Total" por cada fila (año) para permitir análisis de proporción.

### 3. Sistema de Persistencia y Exportación
El módulo garantiza que los resultados del análisis queden registrados de forma histórica.

* **Exportación JSON con Timestamp**: La función `export_stats_to_json` genera archivos en la carpeta `results/` con un nombre único basado en el momento exacto de la ejecución (`stats_YYYYMMDD_HHMMSS.json`).
* **Serialización Robusta**: Uso de `default=str` en el volcado JSON para garantizar que objetos de Python no nativos (como fechas de Pandas) se guarden correctamente sin romper el proceso.
* **Gestión de Directorios**: Creación automática del directorio de resultados si no existe.

### 4. Recuperación de Datos
* **`load_latest_stats`**: Implementación de un buscador de archivos que identifica y carga automáticamente el último reporte estadístico generado, permitiendo retomar análisis previos sin recalcular.

---