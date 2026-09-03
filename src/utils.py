import numpy as np
import pandas as pd

"""Calcula la distancia en kilómetros entre la ubicación del comercio y la del cliente utilizando la fórmula de Haversine. Esto es necesario porque la distancia geográfica no se puede calcular directamente a partir de las coordenadas de latitud y longitud."""
def calculate_distance_km(df):
    EARTH_RADIUS_KM = 6371.0

    lat1 = np.radians(df['lat'])
    lon1 = np.radians(df['long'])
    lat2 = np.radians(df['merch_lat'])
    lon2 = np.radians(df['merch_long'])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


"""Calcula la edad aproximada del titular de la tarjeta restando el año de nacimiento del año de la transacción. Solo se considera el año ya que diferencias de pocos meses no son relevantes para la detección de fraude."""
def calculate_age(df, col_dob="dob", col_trans="trans_date_trans_time"):
    """Calculamos la edad aproximada restándole al año de la transacción el año de nacimiento del titular."""

    # Usar el formato datetime existente si está disponible para evitar conversiones innecesarias
    trans_year = df[col_trans].dt.year if pd.api.types.is_datetime64_any_dtype(df[col_trans]) else pd.to_datetime(df[col_trans]).dt.year
    dob_year = pd.to_datetime(df[col_dob]).dt.year

    return trans_year - dob_year


def transform_cyclic_hour(df, col_trans="trans_date_trans_time"):
    """Calcula las transformaciones de seno y coseno de la hora de la transacción para capturar su naturaleza cíclica."""
    
    hours = pd.to_datetime(df[col_trans]).dt.hour

    sin_hour = np.sin(2 * np.pi * hours / 24)
    cos_hour = np.cos(2 * np.pi * hours / 24)

    return sin_hour, cos_hour