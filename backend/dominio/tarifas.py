# backend/dominio/tarifas.py
from datetime import datetime
from typing import Tuple, Dict, Any
from .geo import haversine_km


def calcular_tarifa(
    origen: Tuple[float, float],
    destino_latlon: Tuple[float, float],
    cfg: Dict[str, Any],
) -> float:
    """
    Tarifa = max( base + por_km * distancia_km , minimo )
    """
    tcfg = cfg.get("tarifa", {})
    base = float(tcfg.get("base", 2.5))
    por_km = float(tcfg.get("por_km", 1.1))
    minimo = float(tcfg.get("minimo", 5.0))

    km = haversine_km(origen, destino_latlon)
    tarifa = base + por_km * km
    if tarifa < minimo:
        tarifa = minimo
    return round(tarifa, 2)


def aplicar_suplementos(
    destino_id: str,
    when: datetime,
    cfg: Dict[str, Any],
    evento_ber: bool = False,
) -> float:
    """
    Suplementos:
      - Aeropuerto (destino_id == 'T4')
      - Nocturno (22–06)
      - Evento Bernabéu (si evento_ber True y destino BER)
    """
    scfg = cfg.get("suplementos", {})
    total = 0.0

    if destino_id == "T4":
        total += float(scfg.get("aeropuerto_T4", 5.0))

    h = when.hour
    if h >= 22 or h < 6:
        total += float(scfg.get("nocturno_22_06", 2.0))

    if destino_id == "BER" and evento_ber:
        total += float(scfg.get("evento_BER", 2.0))

    return round(total, 2)
