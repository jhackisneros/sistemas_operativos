# backend/dominio/geo.py
import math
import random
from typing import Tuple


def haversine_km(origen: Tuple[float, float], destino: Tuple[float, float]) -> float:
    """Distancia aproximada en km entre dos puntos lat/lon."""
    lat1, lon1 = origen
    lat2, lon2 = destino
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def dispersion_latlon(
    centro: Tuple[float, float], radio_metros: float = 500.0
) -> Tuple[float, float]:
    """Devuelve un punto aleatorio alrededor de 'centro' dentro de un radio en metros."""
    lat, lon = centro
    # 1 grado de latitud ~ 111km
    rad_km = radio_metros / 1000.0
    dlat = (random.random() - 0.5) * (rad_km / 111.0) * 2
    dlon = (random.random() - 0.5) * (rad_km / (111.0 * math.cos(math.radians(lat)))) * 2
    return lat + dlat, lon + dlon
