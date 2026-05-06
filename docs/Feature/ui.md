Creado por **Andres Lopez** y documentado por **Israel C. Rojas**

# Documentacion de creacion de ui, de tests y cambios de modularizacion carpeta KPIs/ y de test_kpis.py y test_filters.py

### Index

- [Documentacion de modularizacion de KPIs](#documentacion-de-modularizacion-de-kpis)
  - [render_kpis.py](#render_kpipy)
    - [Resumen](#resumen)
    - [Funcionalidades](#funcionalidades)
  - [_calc_years_covered.py](#_calc_years_coveredpy)
    - [Resumen](#resumen-1)
    - [Funcion](#funcion)
  - [_calc_regions.py](#_calc_regionspy)
    - [Resumen](#resumen-2)
    - [Funcion](#funcion-1)
  - [_calc_pct_minors.py](#_calc_pct_minorspy)
    - [Resumen](#resumen-3)
    - [Funcion](#funcion-2)
  - [_calc_avg_age.py](#_calc_avg_agepy)
    - [Resumen](#resumen-4)
    - [Funcion](#funcion-3)

- [Documentacion de modularizacion de filters](#documentacion-de-modularizacion-de-filters)
  - [render_sidebar.py](#render_sidebarpy)
    - [Resumen](#resumen-5)
    - [Funciones](#funciones)
  - [apply_filters.py](#apply_filterspy)
    - [Resumen](#resumen-6)
    - [Funcion](#funcion-4)

- [Documentacion de tests y sus cambios hechos](#documentacion-de-tests-y-sus-cambios-hechos)
  - [test_kpis.py](#test_kpipy)
    - [Descripcion](#descripcion)
    - [Cambios](#cambios)
  - [test_filters.py](#test_filterspy)
    - [Descripcion](#descripcion-1)
    - [Cambios](#cambios-1)



# Documentacion de modularizacion de KPIs
Se ha modularizado el archivo KPIs.py a archivos separados que se demuestran abajo.

## render_kpis.py
### Resumen     
Esta función construye la fila de KPIs del dashboard en Streamlit a partir de un DataFrame filtrado y el DataFrame original.

### Funcionalidades 

- Define render_kpis(df, df_original) para pintar 5 métricas en una fila horizontal usando st.columns(5) en la cabecera del dashboard.

- Calcula la edad media y el porcentaje de menores de 18 tanto sobre el DataFrame filtrado como sobre el DataFrame original reutilizando las funciones puras _calc_avg_age() y _calc_pct_minors().

- Muestra la métrica “Total fatalidades” con el número de filas filtradas y un delta len(df) - len(df_original) usando delta_color="inverse" para que una reducción de casos se pinte como cambio positivo.

- Muestra “Edad promedio” con el valor medio actual y el delta respecto a la edad media original, también con delta_color="inverse" para considerar mejor una edad media más baja.

- Muestra “% Menores de 18” formateado con un decimal y el delta respecto al porcentaje original, igualmente con delta_color="inverse" para resaltar una reducción de menores fallecidos como algo positivo.

- Calcula y muestra “Años cubiertos” llamando a _calc_years_covered(df) y “Regiones” llamando a _calc_regions(df), sin delta, para indicar el rango temporal y geográfico cubierto por los datos filtrados. 

## _calc_years_covered.py
### Resumen

Es una función de ayuda muy simple que devuelve cuántos años distintos hay en el DataFrame, devolviendo 0 si está vacío.

### Funcion

- Define la función _calc_years_covered(df) que calcula el número de años distintos presentes en la columna year del DataFrame usando df["year"].nunique().

- Antes de contar, comprueba df.empty para devolver 0 cuando el DataFrame está vacío, evitando errores y dejando claro que un dataset sin filas no cubre ningún año.


## _calc_regions.py
### Resumen 
Es otra función de ayuda que cuenta cuántas regiones distintas hay en la columna event_location_region, devolviendo 0 si el DataFrame está vacío.

### Funcion
- Define la función _calc_regions(df) que devuelve el número de regiones únicas presentes en la columna event_location_region usando df["event_location_region"].nunique().

- Comprueba primero df.empty para retornar 0 cuando el DataFrame no tiene filas, evitando accesos innecesarios a columnas y dejando claro que sin datos no hay regiones cubiertas.

## _calc_pct_minors.py
### Resumen
Esta función calcula el porcentaje de víctimas menores de 18 años sobre el total de filas del DataFrame, devolviendo 0.0 si no hay datos.

### Funcion

- Define la función _calc_pct_minors(df) que recibe un DataFrame con una columna numérica age y devuelve el porcentaje de filas con edad menor que 18, en el rango de 0.0 a 100.0.

- Si el DataFrame está vacío (df.empty), devuelve 0.0 directamente; en caso contrario calcula el número de menores como (df["age"] < 18).sum() y lo divide entre len(df), multiplicando por 100 para obtener el porcentaje.

## _calc_avg_age.py
### Resumen
Esta función calcula la edad media de las víctimas, ignorando NaN, y la devuelve redondeada a un decimal; si no hay datos válidos, devuelve 0.0.

### Funcion

- Define la función _calc_avg_age(df) que obtiene la columna age, elimina valores nulos con dropna() y calcula la media de las edades válidas, devolviendo el resultado redondeado a 1 decimal con round(..., 1).

- Si el DataFrame está vacío (df.empty) o, tras eliminar nulos, no queda ninguna edad válida (valid_ages.empty), devuelve 0.0, evitando excepciones y representando la ausencia de datos con un valor neutro.

# Documentacion de modularizacion de filters
## render_sidebar.py
### Resumen
Esta función construye el panel de filtros en la barra lateral de Streamlit y devuelve un diccionario con los valores seleccionados por el usuario para aplicarlos luego al DataFrame.

### Funciones

- Define render_sidebar(df) que pinta en st.sidebar un título “Filtros” y separadores, y a partir de los valores únicos del DataFrame original construye los widgets interactivos para filtrar los datos.

- Calcula el año mínimo y máximo de la columna year y crea un st.sidebar.slider que permite seleccionar un rango de años (year_range) a partir de esos límites.

- Añade cuatro st.sidebar.multiselect: uno para “Ciudadania” con los valores únicos no nulos de df["citizenship"], otro para “Genero” con df["gender"], otro para “Region” con df["event_location_region"] y otro para “Causa de muerte” con df["killed_by"], todos ordenados alfabéticamente.

- Devuelve un diccionario con las claves year_range, citizenship, gender, region y killed_by, que encapsula el estado de los filtros seleccionados y se utilizará después para filtrar el DataFrame.

## apply_filters.py
### Resumen
Esta función aplica de forma pura todos los filtros seleccionados sobre el DataFrame original y devuelve una copia filtrada, registrando al final un log con el resumen del filtrado.

### Funcion

- Define apply_filters(df, filters) como función pura: empieza haciendo df.copy() y nunca modifica el DataFrame original, devolviendo siempre una nueva copia filtrada.

- Si filters["year_range"] no es None, filtra por la columna year usando .between(inicio, fin) para quedarse solo con las filas cuyo año está dentro del rango seleccionado.

- Si las listas de filtros citizenship, gender, region o killed_by no están vacías, filtra cada una de las columnas correspondientes usando .isin(lista) para quedarse solo con las filas cuyos valores pertenecen a las selecciones del usuario.

- Al final, llama a log_filter_applied(log, filters, len(df), len(filtered)) para registrar en el log qué filtros se han aplicado y cuántas filas había antes y después del filtrado, y devuelve el DataFrame filtered.

# Documentacion de tests y sus cambios hechos

## test_kpis.py

### Descripcion
Los tests de **test_kpis.py** validan en presente el comportamiento de las funciones encargadas de calcular KPIs y de la funcion **render_kpis()**. La suite comprueba resultados correctos, casos limite como DataFrames vacios, valores duplicados o valores **NaN**, y tambien verifica que la representacion de KPIs en Streamlit se ejecuta correctamente mediante mocks.

En concreto, los tests comprueban el porcentaje de menores, el numero de años cubiertos, el numero de regiones distintas, la media de edad y la correcta creacion de columnas y metricas en la interfaz. Tambien verifican que **render_kpis()** sigue funcionando cuando recibe un DataFrame filtrado vacio.

### Cambios

- Se cambia el origen del import de las funciones KPI desde **src.kpis** a **src.logger.kpis.kpis** para adaptarlo a la nueva ruta del modulo.
- Se implementan los cuatro tests de la clase **TestCalcPctMinors**, que validan el porcentaje correcto de menores, el caso de DataFrame vacio, el caso sin menores y el caso con todos menores.
- Se implementan los tres tests de la clase **TestCalcYearsCovered**, que validan el numero de años distintos, el comportamiento con DataFrame vacio y el tratamiento correcto de años duplicados.
- Se implementan los dos tests de la clase **TestCalcRegions**, que verifican el numero de regiones distintas y el retorno correcto cuando el DataFrame esta vacio.
- Se implementan los tres tests de la clase **TestCalcAvgAge**, que comprueban la media de edad, el caso de DataFrame vacio y que los valores **NaN** no afecten al calculo.
- Se implementan los tests de la clase **TestRenderKpis**, donde se mockea **st.columns** para devolver cinco columnas y se verifica que **render_kpis()** crea esas cinco columnas, llama una vez a **metric()** en cada una y no falla con un DataFrame filtrado vacio.

## test_filters.py

### Descripcion
Los tests de **test_filters.py** validan en presente el funcionamiento de **apply_filters()** en los principales escenarios de filtrado. La suite comprueba que la funcion filtra correctamente por rango de años, ciudadania, genero, region y autor de la muerte, y tambien valida combinaciones de filtros y casos sin coincidencias.

Ademas, los tests verifican que la funcion siempre devuelve un **DataFrame**, que no modifica el original y que la presencia de valores **NaN** en columnas como **age** no rompe el proceso de filtrado.

### Cambios

- Se implementa **test_no_filters_returns_all_rows**, que ejecuta **apply_filters(sample_df, no_filters)** y comprueba que se devuelven todas las filas del DataFrame original.
- Se implementa **test_year_range_filters_correctly**, que aplica **year_range=(2000, 2010)** y verifica que las filas devueltas estan dentro del rango indicado.
- Se implementa **test_year_range_excludes_outside**, que usa **year_range=(2005, 2005)** y comprueba que solo se devuelve la fila correspondiente a ese año.
- Se implementa **test_citizenship_single**, que aplica el filtro **citizenship=["Palestinian"]** y verifica que todas las filas resultantes tienen esa ciudadania.
- Se implementa **test_citizenship_multiple**, que aplica **citizenship=["Palestinian", "Israeli"]** y comprueba que se aceptan todos los valores esperados.
- Se implementa **test_gender_filter**, que aplica **gender=["Male"]** y verifica que todas las filas devueltas tienen ese genero.
- Se implementa **test_region_filter**, que aplica **region=["West Bank"]** y comprueba que el filtrado por region funciona correctamente.
- Se implementa **test_killed_by_filter**, que aplica **killed_by=["Israeli security forces"]** y verifica que todas las filas devueltas contienen ese valor.
- Se implementa **test_combined_filters**, que combina **year_range=(2000, 2010)** con **citizenship=["Palestinian"]** y comprueba que el resultado coincide con la interseccion esperada.
- Se implementa **test_no_match_returns_empty_df**, que aplica un rango de años sin coincidencias y verifica que el DataFrame resultante queda vacio.
- Se mantienen sin cambios **test_always_returns_dataframe** y **test_does_not_modify_original**, que ya validaban el tipo de retorno y la inmutabilidad del DataFrame original.
- Se añade **test_handles_nan_ages**, que crea un DataFrame con valores **None** en **age** y verifica que el filtrado sigue funcionando correctamente.