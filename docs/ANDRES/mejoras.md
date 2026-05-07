# MODIFICADO `src/filters/render_sidebar.py` PARA AÑADIR EL BOTON DE CARGAR CSV


## 1. Nuevo archivo: src/data_loader/column_mapping.py
- Funciones para mapeo inteligente de columnas usando similitud de cadenas
- Algoritmo que considera: similitud de secuencia, coincidencia de palabras y tokens importantes
- Funciones: find_column_mapping(), apply_column_mapping(), get_unmapped_columns()
## 2. Modificado: src/filters/render_sidebar.py
- Añadido botón de carga CSV en la parte superior del sidebar
- Mapeo automático de columnas al subir un archivo
- Interfaz para mapeo manual cuando no hay coincidencia automática
- Los datos se guardan en st.session_state.additional_data
## 3. Modificado: app.py
- Función combine_data() para combinar datos originales con adicionales
- Los datos combinados se usan en toda la aplicación
### Cómo probar:
- Ejecuta la app: streamlit run app.py
- En el sidebar, sube un CSV usando "📁 Añadir datos CSV"
- El sistema mapeará automáticamente columnas similares (ej: full_name → name, event_date → date_of_event)
- Si hay columnas sin mapear, selecciónalas manualmente
- Haz clic en "✅ Confirmar y añadir datos"
### Archivo de prueba creado: data/test_additional.csv

----------------

## El mapeo ahora funciona con el formato de columnas siguiente. Todas las columnas se mapean correctamente:
````
Name → name
Date_of_event → date_of_event
Citizenship → citizenship
Event_location_District → event_location_district
etc.
````
## Ahora se puede subir un CSV con separador ; y el sistema:

- Detecta automáticamente el separador
- Normaliza los nombres de columnas (espacios y guiones a _)
- Mapea automáticamente las columnas por similitud
- Te permite ajustar manualmente cualquier columna no reconocida


## Ahora cuando subas un CSV, el sistema:

- Detecta duplicados comparando name + date_of_event/date_of_death
- Muestra advertencia con cantidad de duplicados encontrados
- Opción para eliminar duplicados antes de añadir con el botón "🗑️ Eliminar duplicados y añadir"
- Opción para añadir todos los datos (incluyendo duplicados) con "✅ Confirmar y añadir datos"

### También se mantienen las funcionalidades anteriores:

- Detección automática de separador (coma o punto y coma)
- Mapeo automático de columnas por similitud
- Mapeo manual cuando sea necesario


## Pagina de donde se sacaron alguno de los csv añadidos 
https://statistics.btselem.org/en/all-fatalities/by-date-of-incident?section=overall&tab=overview 
