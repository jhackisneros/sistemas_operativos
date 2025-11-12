# backend/dominio/tiempo_sim.py
import time
from datetime import datetime, timedelta


class TiempoSim:
    """
    Reloj simulado:
      - escala: 1s real = escala segundos simulados (por defecto 288: 5min -> 24h)
      - ahora(): devuelve datetime simulado
    """
    def __init__(self, escala: int = 288):
        self.escala = int(escala)
        self._t0_real = time.time()
        # Punto de inicio “virtual” del tiempo simulado (ajústalo si quieres)
        self._t0_sim = datetime(2025, 1, 1, 8, 0, 0)

    def ahora(self) -> datetime:
        dt_real = time.time() - self._t0_real
        dt_sim = dt_real * self.escala
        return self._t0_sim + timedelta(seconds=dt_sim)


# Singleton global para usar en todo el backend
TIEMPO = TiempoSim()
