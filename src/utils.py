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

def preprocess_for_anomaly_detection(X_raw, freq_maps=None):
    """Usamos la misma frecuencia de train aunque llamemos la función con test para evitar data leakage"""

    # Columnas categóricas que se van a transformar en frecuencias
    cols_freq = ["category", "job", "state", "merchant"]
    # Columnas que se eliminan al final (identificadores, PII, ya procesadas)
    cols_to_drop = [
        "category", "job", "state", "merchant",
        "trans_date_trans_time", "lat", "long",
        "merch_lat", "merch_long", "dob",
        "street", "city", "zip", "unix_time",
        "first", "last", "cc_num", "trans_num", "Unnamed: 0",
    ]

    # Copiamos el dataframe para no modificar el original por accidente
    X = X_raw.copy()
    X['trans_date_trans_time'] = pd.to_datetime(X['trans_date_trans_time'])

    # Creamos las variables derivadas: hora cíclica, distancia, edad, género binario
    X["hour_sin"], X["hour_cos"] = transform_cyclic_hour(X)
    X["distance_km"] = calculate_distance_km(X)
    X["age"] = calculate_age(X)
    X['gender'] = X['gender'].map({'F': 0, 'M': 1})

    # El diccionario va a guardar las frecuencias SOLO si las estamos calculando (train)
    computed_freq_maps = {}
    for col in cols_freq:
        if freq_maps is None:
            # Caso TRAIN: no nos pasaron frecuencias de antemano,
            # así que las calculamos desde cero con los datos actuales
            freq_map = X[col].value_counts(normalize=True)
            computed_freq_maps[col] = freq_map
        else:
            # Caso TEST: ya nos pasaron un freq_maps calculado en train,
            # así que reutilizamos ESE en vez de calcular uno nuevo con datos de test
            freq_map = freq_maps[col]
        
        # En ambos casos, usamos el freq_map (nuevo o reutilizado) para crear la columna
        X[f"{col}_freq"] = X[col].map(freq_map)
        # Valores nuevos en test que no existían en train → frecuencia 0
        X[f"{col}_freq"] = X[col].map(freq_map).fillna(0)
    
    # Aplicamos log(1+x) al monto para reducir el sesgo de valores muy altos
    X["amt"] = np.log1p(X["amt"])
    # Eliminamos las columnas que ya no sirven (categóricas originales, PII, etc.)
    X = X.drop(columns=cols_to_drop, errors="ignore")

    # Devolvemos siempre 2 cosas: 1) el dataframe ya procesado y # 2) el diccionario de frecuencias
    return X, (computed_freq_maps if freq_maps is None else freq_maps)