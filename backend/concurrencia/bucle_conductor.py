# backend/concurrencia/bucle_conductor.py
import threading
import time
import random
from datetime import datetime

from almacenamiento.repositorio import Repositorio
from dominio.modelos import EstadoTaxi, EstadoViaje, EstadoConductor
from dominio.geo import haversine_km


class BucleConductor:
    """
    Simula el comportamiento del taxi:
      - Si tiene viaje ASIGNADO -> lo INICIA tras breve espera
      - Calcula una duración basada en distancia y finaliza el viaje
      - Libera taxi a LIBRE
    Nota: es opcional; en un backend real, esto viene desde la app del conductor.
    """
    def __init__(self, repo: Repositorio, velocidad_kmh: float | None = None):
        self.repo = repo
        self.vel_kmh = velocidad_kmh or self.repo.cfg.get("velocidad_kmh", 25.0)
        self._hilos: dict[str, tuple[threading.Thread, threading.Event]] = {}  # conductor_id -> (th, stop)

    def iniciar_para_conductor(self, conductor_id: str):
        if conductor_id in self._hilos:
            return
        stop = threading.Event()
        th = threading.Thread(target=self._loop, args=(conductor_id, stop), daemon=True)
        self._hilos[conductor_id] = (th, stop)
        th.start()

    def detener_para_conductor(self, conductor_id: str):
        if conductor_id in self._hilos:
            th, stop = self._hilos.pop(conductor_id)
            stop.set()

    def _loop(self, conductor_id: str, stop: threading.Event):
        # Busca el taxi del conductor
        taxi = self.repo.obtener_taxi_por_conductor(conductor_id)
        if not taxi:
            return

        while not stop.wait(timeout=1.0):
            c = self.repo.obtener_conductor(conductor_id)
            if not c or c.estado != EstadoConductor.ONLINE:
                continue

            # Encuentra viajes asignados a este taxi
            pendientes = [v for v in self.repo.viajes.values()
                          if v.taxi_id == taxi.id and v.estado == EstadoViaje.ASIGNADO]

            for vj in pendientes:
                # Simula que el conductor acepta y empieza el viaje
                time.sleep(random.uniform(0.2, 1.0))  # tiempo de recogida breve
                self.repo.marcar_inicio_viaje(vj.id, ts=datetime.utcnow())

                # Duración simulada ~ distancia / vel (en minutos → segundos)
                destino_latlon = self.repo.destinos[vj.destino_id]
                km = haversine_km(vj.origen, destino_latlon)
                mins = max(2.0, (km / self.vel_kmh) * 60.0)  # mínimo 2 min simulados
                time.sleep(mins / 60.0)  # escala real (puedes multiplicar por un factor si quieres más rápido)

                # Finaliza viaje: suma ganancias y libera taxi
                self.repo.marcar_fin_viaje(vj.id, ts=datetime.utcnow())
                # taxi queda LIBRE desde repositorio.marcar_fin_viaje()
