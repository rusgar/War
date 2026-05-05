Angel Echenique visualizacion

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
- **Nivel interno**: Ciudadanía (Palestinian, Israeli, Foreign, Jordanian)
- **Nivel externo**: Género (M, F)

### Implementación
```python
df_plot = df.copy()
df_plot = df_plot.dropna(subset=["gender"])

colors_gender = {"M": "#3A86FF", "F": "#FF006E"}

fig = px.sunburst(
    df_plot,
    path=["citizenship", "gender"],
    title="Distribución por Ciudadanía y Género",
    color="gender",
    color_discrete_map=colors_gender,
)

fig.update_traces(
    textinfo="label+percent entry",
    textfont=dict(size=14, color="white"),
    marker=dict(line=dict(color="white", width=2))
)

fig.update_layout(
    font=dict(size=16),
    title_font=dict(size=20, color="#333"),
    margin=dict(t=80, l=20, r=20, b=20),
    width=600,
    height=600
)
```

### Colores por Género
| Género | Color |
|--------|-------|
| Masculino (M) | Azul `#3A86FF` |
| Femenino (F) | Rosa `#FF006E` |

### Estilo Profesional
- Texto en blanco con borde para visibilidad
- Tamaño de fuente: 14px en etiquetas, 20px en título
- Círculo de 600x600px
- Bordes blancos entre segmentos

### Logging
```python
log_chart_rendered(log, "chart_gender_breakdown", len(df))
```