# backend/dominio/geo.py
import math
import random
from typing import Tuple


def haversine_km(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """
    Distancia Haversine entre dos puntos (lat, lon) en km.
    """
    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    la1 = math.radians(lat1)
    la2 = math.radians(lat2)
    x = math.sin(dlat / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def dispersion_latlon(lat: float, lon: float, radio_m: int = 800) -> Tuple[float, float]:
    """
    Devuelve un punto aleatorio alrededor de (lat, lon) dentro de un círculo de 'radio_m' metros.
    """
    r = radio_m * math.sqrt(random.random())  # para distribución uniforme en área
    theta = random.random() * 2 * math.pi
    dlat = (r * math.cos(theta)) / 111_111.0
    dlon = (r * math.sin(theta)) / (111_111.0 * math.cos(math.radians(lat)))
    return lat + dlat, lon + dlon
