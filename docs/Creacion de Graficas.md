# Creacion de las Graficas (5 y 7) [Carlos]

**Fecha:** 06/05/2026

## Grafica 5 (linea 374 a 419)

def chart_by_region(df: pd.DataFrame) -> go.Figure:
    """
    Barras horizontales apiladas: region vs fatalidades por ciudadania.
    """
    # 1. Agrupar y contar fatalidades por región y ciudadanía
    df_counts = (
        df.groupby(["event_location_region", "citizenship"])
        .size()
        .reset_index(name="count")
    )

    # 2. Calcular el total por región para ordenar el eje Y de forma descendente
    region_totals = (
        df_counts.groupby("event_location_region")["count"]
        .sum()
        .sort_values(ascending=True) # Ascendente para que la más alta quede arriba en el gráfico H
        .index
    )

    # 3. Crear el gráfico de barras horizontales apiladas
    fig = px.bar(
        df_counts,
        y="event_location_region",
        x="count",
        color="citizenship",
        orientation="h",
        barmode="stack",
        color_discrete_map=PALETTE,
        category_orders={"event_location_region": list(region_totals)},
        labels={
            "event_location_region": "Región",
            "count": "Número de Fatalidades",
            "citizenship": "Ciudadanía"
        },
        title="<b>Fatalidades por Región</b>"
    )

    # Ajustes estéticos adicionales
    fig.update_layout(
        xaxis_title="Fatalidades",
        yaxis_title=None,
        legend_title="Ciudadanía",
        hovermode="y unified"
    )

    return fig

## Grafica 7 (linea 489 a 546)

def chart_killed_by(df: pd.DataFrame) -> go.Figure:
    """
    Genera un Donut Chart de fatalidades y un Bar Chart de evolución temporal.
    """
    # 1. Preparación de datos para el Donut (Proporción total)
    counts = df["killed_by"].value_counts().reset_index()
    counts.columns = ["causa", "total"]

    # 2. Preparación de datos para el Reto (Evolución temporal)
    df['date_parsed'] = pd.to_datetime(df['date_of_event'], errors='coerce')
    df['year_month'] = df['date_parsed'].dt.to_period('M').astype(str)
    evolution = df.groupby(['year_month', 'killed_by']).size().reset_index(name='counts')

    # Crear subplots: 1 fila, 2 columnas
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "domain"}, {"type": "xy"}]],
        subplot_titles=("Distribución Total", "Evolución Temporal")
    )

    # Gráfico de Dona (Pie con hole)
    fig.add_trace(
        go.Pie(
            labels=counts["causa"],
            values=counts["total"],
            hole=0.45,
            name="Fatalidades",
            textinfo='percent+label',
            textfont=dict(size=16)
        ),
        row=1, col=1
    )

    # Gráfico de Barras (Evolución)
    for killer in df["killed_by"].unique():
        killer_data = evolution[evolution["killed_by"] == killer]
        fig.add_trace(
            go.Bar(
                x=killer_data["year_month"],
                y=killer_data["counts"],
                name=str(killer)
            ),
            row=1, col=2
        )

    # Diseño y Estética
    fig.update_layout(
        title_text="<b>Quién causó las fatalidades</b>",
        template="plotly_white",
        legend_title="Causa",
        barmode='stack',
        height=600,
        width=1100,
        font=dict(size=14),
        title_font=dict(size=20)
    )

    return fig