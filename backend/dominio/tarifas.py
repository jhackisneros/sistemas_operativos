# backend/dominio/tarifas.py
from typing import Tuple, Dict
from datetime import datetime
from backend.dominio.geo import haversine_km


def calcular_tarifa(
    origen: Tuple[float, float],
    destino: Tuple[float, float],
    cfg: Dict,
) -> float:
    """
    Tarifa base + km. Si cfg está vacío, se usan valores por defecto.
    """
    tarifa_base = cfg.get("tarifa_base", 3.0)
    precio_km = cfg.get("precio_km", 1.2)

    km = haversine_km(origen, destino)
    return tarifa_base + precio_km * km


def aplicar_suplementos(
    destino_id: str,
    cuando: datetime,
    cfg: Dict,
    evento_ber: bool = False,
) -> float:
    """
    Aplica suplementos sencillos:
      - nocturno (22:00–6:00)
      - especial T4
    """
    hora = cuando.hour
    suplemento_nocturno = cfg.get("suplemento_nocturno", 1.0)
    suplemento_t4 = cfg.get("suplemento_t4", 5.0)

    total = 0.0

    # nocturno
    if hora >= 22 or hora < 6:
        total += suplemento_nocturno

    # aeropuerto T4
    if destino_id == "T4":
        total += suplemento_t4

    return total
