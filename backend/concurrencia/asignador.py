# backend/concurrencia/asignador.py
import threading
import heapq
from datetime import datetime
from typing import List, Tuple
import asyncio

from almacenamiento.repositorio import Repositorio
from dominio.modelos import EstadoTaxi, EstadoViaje
from eventos.ws import notificar_asignacion


class AsignadorMonitor:
    """
    Monitor que empareja solicitudes con taxis libres.
    """
    def __init__(self, repo: Repositorio):
        self.repo = repo
        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)

    def submit(self, viaje_id: str) -> None:
        with self._cv:
            self._cv.notify()

    def _candidatos(self, origen: tuple) -> List[Tuple[float, float, str]]:
        from dominio.geo import haversine_km
        out = []
        for taxi_id, taxi in self.repo.taxis.items():
            if taxi.estado != EstadoTaxi.LIBRE or not taxi.ubicacion:
                continue
            d = haversine_km(origen, taxi.ubicacion)
            out.append((d, -taxi.rating, taxi_id))
        return out

    def loop(self):
        while True:
            with self._cv:
                while not self.repo.cola_solicitudes:
                    self._cv.wait(timeout=0.5)
                viaje_id = self.repo.pop_solicitud()

            if not viaje_id:
                continue

            vj = self.repo.obtener_viaje(viaje_id)
            if not vj or vj.estado != EstadoViaje.PENDIENTE:
                continue

            candidatos = self._candidatos(vj.origen)
            if not candidatos:
                with self._cv:
                    self.repo.push_solicitud(viaje_id)
                    self._cv.wait(timeout=0.5)
                continue

            heapq.heapify(candidatos)
            _, _, taxi_id = heapq.heappop(candidatos)
            taxi = self.repo.taxis[taxi_id]
            if taxi.estado != EstadoTaxi.LIBRE:
                with self._cv:
                    self.repo.push_solicitud(viaje_id)
                continue

            # Actualiza estado
            self.repo.actualizar_estado_taxi(taxi_id, EstadoTaxi.ASIGNADO)
            self.repo.marcar_asignado(viaje_id, taxi_id, ts=datetime.utcnow())

            # Notificar evento WS
            try:
                asyncio.get_running_loop().create_task(notificar_asignacion(viaje_id))
            except RuntimeError:
                pass


def iniciar_asignador(repo: Repositorio) -> AsignadorMonitor:
    """
    Inicializa el monitor de asignación en un hilo daemon.
    """
    mon = AsignadorMonitor(repo)
    repo.asignador = mon
    t = threading.Thread(target=mon.loop, daemon=True)
    t.start()
    return mon
