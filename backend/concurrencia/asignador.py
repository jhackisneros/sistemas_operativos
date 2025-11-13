# backend/concurrencia/asignador.py
import threading
import time
from typing import Optional

from backend.almacenamiento.repositorio import Repositorio
from backend.dominio.modelos import EstadoTaxi, EstadoViaje


class Asignador(threading.Thread):
    """
    Hilo que toma viajes PENDIENTES y los asigna al taxi LIBRE más cercano.
    """

    def __init__(self, repo: Repositorio, intervalo_seg: float = 1.0) -> None:
        super().__init__(daemon=True)
        self.repo = repo
        self.intervalo_seg = intervalo_seg
        self._parar = threading.Event()

    def detener(self) -> None:
        self._parar.set()

    def _buscar_taxi_libre_mas_cercano(self, viaje_id: str) -> Optional[str]:
        v = self.repo.obtener_viaje(viaje_id)
        if not v:
            return None
        origen = v.origen

        mejor_taxi_id = None
        mejor_dist = None

        for t in self.repo.taxis.values():
            if t.estado != EstadoTaxi.LIBRE:
                continue
            dist = self.repo.cfg.get("funcion_distancia", None)
            # usamos haversine_km directo desde repo
            from backend.dominio.geo import haversine_km

            d = haversine_km(origen, t.ubicacion)
            if mejor_dist is None or d < mejor_dist:
                mejor_dist = d
                mejor_taxi_id = t.id

        return mejor_taxi_id

    def run(self) -> None:
        while not self._parar.is_set():
            viaje_id = self.repo.pop_solicitud()
            if viaje_id is None:
                time.sleep(self.intervalo_seg)
                continue

            taxi_id = self._buscar_taxi_libre_mas_cercano(viaje_id)
            if taxi_id:
                self.repo.marcar_asignado(viaje_id, taxi_id)
                # marcamos taxi como OCUPADO
                self.repo.actualizar_estado_taxi(taxi_id, EstadoTaxi.OCUPADO)
            else:
                # no hay taxi, devolvemos el viaje a la cola
                self.repo.push_solicitud(viaje_id)
                time.sleep(self.intervalo_seg)


_asignador_global: Optional[Asignador] = None


def iniciar_asignador(repo: Repositorio) -> None:
    global _asignador_global
    if _asignador_global is None:
        _asignador_global = Asignador(repo)
        repo.asignador = _asignador_global
        _asignador_global.start()
