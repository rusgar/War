Creado por **Andres Lopez** y documentado por **Israel C. Rojas**

# Documentacion de creacion, de tests y cambios de los archivos test_kpis.py y test_filters.py

## Index

- [Documentacion de cambios de test_kpis.py](#documentacion-de-cambios-de-test_kpipy)
  - [Descripcion](#descripcion)
  - [Cambios](#cambios)
- [Documentacion de cambios de test_filters.py](#documentacion-de-cambios-de-test_filterspy)
  - [Descripcion](#descripcion-1)
  - [Cambios](#cambios-1)

## Documentacion de cambios de **test_kpis.py**

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

## Documentacion de cambios de **test_filters.py**

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