# render_sidebar.py

## Visión General
Función que construye la barra lateral del dashboard con controles de filtro para el usuario.

**Archivo:** `src/filters/render_sidebar.py`  
**Función principal:** `render_sidebar(df: pd.DataFrame) -> dict`  
**Tecnología:** Streamlit

---

## Estructura de la Barra Lateral

### 1. Imagen de Portada
```
📊 Panel de Control
├── Imagen: "filters/img/Portada.png" (si existe)
└── Advertencia si no se encuentra la imagen
```
- Muestra una imagen de portada en la parte superior
- Si la imagen no existe, muestra un warning

### 2. Temporalidad
```
📅 Temporalidad
└── Slider de rango de años (min_year - max_year)
```
- Slider para seleccionar el rango de años a filtrar
- Clave en session_state: `year_slider`

### 3. Perfil de la Víctima (expandido por defecto)
```
👤 Perfil de la Víctima
├── Ciudadanía (multiselect)
└── Género (multiselect)
```
- Claves en session_state: `citiz_filter`, `gender_filter`

### 4. Ubicación y Causa (colapsado por defecto)
```
📍 Ubicación y Causa
├── Región (multiselect)
└── Causa de muerte / Responsable (multiselect)
```
- Claves en session_state: `region_filter`, `cause_filter`

### 5. Botón de Limpieza
```
[ Limpiar todos los filtros ] ← botón primary
```
- Usa `on_click` callback para resetear todos los filtros

---

## Función de Reset (Callback)

```python
def reset_all_filters():
    st.session_state.year_slider = (año_min, año_max)
    st.session_state.citiz_filter = []
    st.session_state.gender_filter = []
    st.session_state.region_filter = []
    st.session_state.cause_filter = []
```

Restaura todos los filtros a sus valores por defecto:
- Años: rango completo
- Ciudadanía, Género, Región, Causa: vacío (sin filtro)

---

## Valor de Retorno

```python
return {
    "year_range": (año_min, año_max),      # tupla
    "citizenship": [...],                    # lista
    "gender": [...],                         # lista
    "region": [...],                         # lista
    "killed_by": [...],                      # lista
}
```

Diccionario con todos los filtros seleccionados, listo para aplicar al DataFrame.

---

## Flujo de Datos

```
Usuario interactúa con sidebar
        │
        ▼
render_sidebar() captura selecciones
        │
        ▼
Devuelve dict con filtros
        │
        ▼
app.py/main.py aplica filtros al DataFrame
        │
        ▼
Dashboard se actualiza
```

---

## Cambios Realizados

| Cambio | Descripción |
|--------|-------------|
| **Imagen portada** | Se agregó carga de imagen `Portada.png` con manejo de error |
| **Callback reset** | Se cambió a `on_click` en vez de lógica manual |
| **Expanders** | Perfil expandido por defecto; Ubicación colapsado |
| **Session state** | Claves definidas con prefijos claros (`year_slider`, `citiz_filter`, etc.) |
| **Logging** | Import de `log_filter_applied` (listo para integrar) |
