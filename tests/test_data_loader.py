import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch
from src.data_loader._normalize_columns import _normalize_columns
from src.data_loader._apply_type_conversions import _apply_type_conversions
from src.data_loader._add_derived_features import _add_derived_features
from src.data_loader.load_data import load_data
# Fixture para crear un DataFrame "sucio" de ejemplo
@pytest.fixture
def raw_df():
    data = {
        "Date of Event": ["2023-10-01", "invalid-date"],
        "Date of Death": ["2023-10-02", "2023-10-03"],
        "Age": ["25", "invalid"],
        "Gender": ["M", "F"],
        "Place of Residence": ["City A", "City B"]
    }
    return pd.DataFrame(data)

def test_normalize_columns(raw_df):
    """Verifica que las columnas se conviertan a snake_case y sin espacios."""
    df_normalized = _normalize_columns(raw_df.copy())
    
    assert "date_of_event" in df_normalized.columns
    assert "place_of_residence" in df_normalized.columns
    assert "Date of Event" not in df_normalized.columns

def test_apply_type_conversions(raw_df):
    """Verifica la conversión de fechas, números y mapeo de género."""
    # Primero normalizamos para que las funciones encuentren las columnas
    df = _normalize_columns(raw_df.copy())
    df_converted = _apply_type_conversions(df)
    
    # Verificar Fechas
    assert pd.api.types.is_datetime64_any_dtype(df_converted["date_of_event"])
    assert pd.isna(df_converted.loc[1, "date_of_event"])  # Fecha inválida -> NaT
    
    # Verificar Edad
    assert pd.api.types.is_numeric_dtype(df_converted["age"])
    assert df_converted.loc[0, "age"] == 25
    
    # Verificar Género
    assert df_converted.loc[0, "gender"] == "Male"
    assert df_converted.loc[1, "gender"] == "Female"

def test_add_derived_features():
    """Verifica la creación de columnas de tiempo y grupos de edad."""
    data = {
        "date_of_event": pd.to_datetime(["2021-05-20", "1990-01-01"]),
        "age": [15, 65]
    }
    df = pd.DataFrame(data)
    df_derived = _add_derived_features(df)
    
    # Verificar componentes de fecha
    assert df_derived.loc[0, "year"] == 2021
    assert df_derived.loc[0, "month_name"] == "May"
    
    # Verificar grupos de edad
    assert df_derived.loc[0, "age_group"] == "Minor (0-17)"
    assert df_derived.loc[1, "age_group"] == "Senior (60+)"

@patch("src.data_loader.load_data.pd.read_csv")
@patch("src.data_loader.load_data.Path.exists")
def test_load_data_success(mock_exists, mock_read_csv, raw_df):
    """Prueba el orquestador load_data simulando la existencia del archivo."""
    mock_exists.return_value = True
    mock_read_csv.return_value = raw_df
    
    df_result = load_data(Path("fake_path.csv"))
    
    # Verificar que el pipeline se ejecutó (buscando una columna normalizada y una derivada)
    assert "date_of_event" in df_result.columns  # De _normalize_columns
    assert "age_group" in df_result.columns      # De _add_derived_features
    assert not df_result.empty

def test_load_data_file_not_found():
    """Verifica que se lance FileNotFoundError si el path no existe."""
    with pytest.raises(FileNotFoundError):
        load_data(Path("non_existent_file.csv"))