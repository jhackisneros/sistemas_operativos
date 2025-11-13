# backend/dominio/tiempo_sim.py
from datetime import datetime, timedelta


class TiempoSimulado:
    """
    5 minutos reales = 24h simuladas.
    ESCALA = 24h / (5/60 h) = 288
    """

    ESCALA = 288.0

    def __init__(self) -> None:
        self._real_inicio = datetime.utcnow()
        self._sim_inicio = datetime(2025, 1, 1, 0, 0, 0)

    def ahora(self) -> datetime:
        ahora_real = datetime.utcnow()
        delta_real = ahora_real - self._real_inicio
        delta_sim = timedelta(seconds=delta_real.total_seconds() * self.ESCALA)
        return self._sim_inicio + delta_sim


TIEMPO = TiempoSimulado()
