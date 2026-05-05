import pandas as pd
from src.charts import chart_fatalities_over_time

def main():
    # Cargar el dataset
    df = pd.read_csv('./data/fatalities.csv')

    # Generar la gráfica
    fig = chart_fatalities_over_time(df)

    # Mostrar la gráfica
    fig.show()

if __name__ == "__main__":
    main()