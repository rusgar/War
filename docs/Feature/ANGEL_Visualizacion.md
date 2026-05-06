Angel Echenique - Visualización

# Gráficos Implementados

## Gráfico 2: Fatalidades por Mes y Año (Heatmap)

**Función:** `chart_monthly_heatmap(df: pd.DataFrame) -> go.Figure`

### Descripción
Muestra la distribución de fatalidades en una matriz donde:
- **Eje X**: Meses del año (Ene-Dic)
- **Eje Y**: Años (2000-2023)
- **Color**: Intensidad de fatalidades

### Implementación
```python
pivot = df.groupby(["year", "month"]).size().unstack(fill_value=0)
fig = go.Figure(data=go.Heatmap(
    z=pivot.values,
    x=MONTHS_ES,
    y=pivot.index,
    colorscale=[[0, "#FFFF00"], [0.25, "#0053EC"], [0.5, "#04FF04"], [1, "#FF0000"]],
    hovertemplate="Año: %{y}<br>Mes: %{x}<br>Fatalidades: %{z}<extra></extra>"
))
```

### Colores (Escala personalizada)
| Nivel | Color | Significado |
|-------|-------|--------------|
| 0% | Amarillo `#FFFF00` | Pocas fatalidades |
| 25% | Azul `#0053EC` | Fatalidades medias-bajas |
| 50% | Verde `#04FF04` | Fatalidades medias-altas |
| 100% | Rojo `#FF0000` | Máxima actividad |

### Logging
```python
log_chart_rendered(log, "chart_monthly_heatmap", len(df))
```

---

## Gráfico 4: Distribución por Ciudadanía y Género (Sunburst)

**Función:** `chart_gender_breakdown(df: pd.DataFrame) -> go.Figure`

### Descripción
Gráfico sunburst de dos niveles:
- **Nivel interno**: Ciudadanía (Palestinian, Israeli, Foreign, Jordanian, American)
- **Nivel externo**: Género (M, F)

### Implementación Actual
```python
df_plot = df.copy()
df_plot = df_plot.dropna(subset=["gender"])

total = len(df_plot)
title = f"Distribución por Ciudadanía y Género ({total:,} registros)"

fig = px.sunburst(
    df_plot,
    path=["citizenship", "gender"],
    title=title,
    color="citizenship",
    color_discrete_map=PALETTE,
    hover_data={"gender": True, "citizenship": False},
)

fig.update_traces(
    textinfo="label+percent entry",
    textfont=dict(size=24, color="black"),
    marker=dict(line=dict(color="white", width=2)),
    hovertemplate="<b>%{label}</b><br>Registros: %{value}<br>Porcentaje: %{percentEntry}<extra></extra>"
)

fig.update_layout(
    font=dict(size=16),
    title_font=dict(size=20, color="#333"),
    margin=dict(t=80, l=20, r=20, b=20),
    width=600,
    height=600,
    legend=dict(
        title="Ciudadanía",
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    )
)
```

### PALETTE (Colores por Ciudadanía)
```python
PALETTE = {
    "Palestinian": "#000080",   # Azul marino
    "Israeli": "#FC0000",        # Rojo
    "Foreign": "#FF009D",        # Rosa
    "Jordanian": "#0053EC",      # Azul
    "American": "#FBFF00",        # Amarillo
}
```

### Cambios Realizados (por el usuario)

| Cambio | Valor Anterior | Valor Nuevo |
|--------|----------------|-------------|
| Color Palestinian | Verde `#04FF04` | El mismo porque  me gusto.
| Tamaño de texto | 14px | 24px |
| Color del texto | Blanco | Negro |
| Título dinámico | Estático | Incluye total de registros: "(11,104 registros)" |
| Tooltip | Básico | Muestra registros y porcentaje |
| Leyenda | No visible | Debajo del gráfico, horizontal |

### Estilo Final
- **Texto**: 24px, color negro, Arial Black
- **Bordes**: Blancos, 2px de ancho
- **Título**: 20px, incluye total de registros
- **Gráfico**: 600x600px
- **Leyenda**: Debajo del gráfico, horizontal

### Datos en el Dataset
| Ciudadanía | Registros |
|------------|-----------|
| Palestinian | 10,092 |
| Israeli | 1,029 |
| Jordanian | 2 |
| American | 1 |

### Logging
```python
log_chart_rendered(log, "chart_gender_breakdown", len(df))
```

---

## Gráfico Scatter 3D (Extra)

**Función:** `chart_scatter_3d(df: pd.DataFrame) -> go.Figure`

### Descripción
Visualización 3D interactiva:
- **Eje X**: Año (2000-2023)
- **Eje Y**: Mes (1-12)
- **Eje Z**: Edad (0-110)
- **Color**: Ciudadanía
- **Símbolo**: Género

### Implementación
```python
df_plot = df[df["age"].between(0, 110)].copy()

if len(df_plot) > 2000:
    df_plot = df_plot.sample(n=2000, random_state=42)

fig = px.scatter_3d(
    df_plot,
    x="year",
    y="month",
    z="age",
    color="citizenship",
    color_discrete_map=PALETTE,
    symbol="gender",
    title="Visualización 3D: Año / Mes / Edad",
    labels={"year": "Año", "month": "Mes", "age": "Edad"},
    hover_data=["event_location_region"],
    opacity=0.8
)
```

### Logging
```python
log_chart_rendered(log, "chart_scatter_3d", len(df))
```