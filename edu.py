import pandas as pd

# Cargar tu CSV
df = pd.read_csv('data/fatalities.csv')  # Cambia por la ruta de tu archivo

# Ver las primeras filas para identificar la columna de distritos
print("Columnas disponibles:")
print(df.columns.tolist())
print("\nPrimeras 5 filas:")
print(df.head())

# Identificar la columna que contiene los distritos (asumiendo que se llama 'district' o similar)
# Puede llamarse: 'district', 'distrito', 'region', 'location', 'area', etc.

# Buscar columnas que podrían contener distritos
possible_district_cols = ['district', 'distrito', 'region', 'location', 'area', 'governorate', 'province']
existing_cols = [col for col in possible_district_cols if col in df.columns]

if existing_cols:
    district_col = existing_cols[0]
    print(f"\nUsando columna: {district_col}")
    
    # Extraer distritos únicos
    unique_districts = df[district_col].unique()
    print(f"\nDistritos únicos encontrados ({len(unique_districts)}):")
    for i, district in enumerate(sorted(unique_districts), 1):
        print(f"{i}. {district}")
    
    # Contar fatalidades por distrito
    district_counts = df.groupby(district_col).size().reset_index(name='total_fatalities')
    district_counts = district_counts.sort_values('total_fatalities', ascending=False)
    
    print("\nTop 10 distritos con más fatalidades:")
    print(district_counts.head(10))
    
    # Ver también por ciudadanía
    district_citizenship = df.groupby([district_col, 'citizenship']).size().reset_index(name='count')
    print("\nEjemplo de datos por distrito y ciudadanía:")
    print(district_citizenship.head(15))
    
else:
    print("\n⚠️ No se encontró una columna de distritos evidente.")
    print("Por favor, revisa los nombres de las columnas manualmente:")
    print(df.columns.tolist())