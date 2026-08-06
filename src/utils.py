import numpy as np
import pandas as pd

# Calculate the distance between the merchant's location ('merch_lat', 'merch_long')
# and the cardholder's registered address ('lat', 'long') using the Haversine formula.
# This calculation is required because geographic distance cannot be computed directly # from latitude and longitude coordinates.
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


# Calculate the approximate age of the cardholder at the time of the transaction.
# Only the year is considered because differences of a few months are not relevant for fraud detection purposes.
def calculate_age(df, col_dob="dob", col_trans="trans_date_trans_time"):
    """Calculate approximate age by subtracting birth year from transaction year."""

    # Use the existing datetime format if available to avoid unnecessary conversions
    trans_year = df[col_trans].dt.year if pd.api.types.is_datetime64_any_dtype(df[col_trans]) else pd.to_datetime(df[col_trans]).dt.year
    dob_year = pd.to_datetime(df[col_dob]).dt.year

    return trans_year - dob_year


def transform_cyclic_hour(df, col_trans="trans_date_trans_time"):
    """Calculate sine and cosine transformations of transaction hour to capture its cyclical nature."""
    
    hours = pd.to_datetime(df[col_trans]).dt.hour

    sin_hour = np.sin(2 * np.pi * hours / 24)
    cos_hour = np.cos(2 * np.pi * hours / 24)

    return sin_hour, cos_hour