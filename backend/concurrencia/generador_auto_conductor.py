# backend/concurrencia/generador_auto_conductor.py
import threading
import time
import random
from typing import Dict

from backend.almacenamiento.repositorio import Repositorio
from backend.dominio.geo import dispersion_latlon
from backend.dominio.tiempo_sim import TIEMPO
from backend.dominio.modelos import EstadoConductor


class GeneradorAutoConductor:
    """
    Para cada conductor ONLINE, genera de vez en cuando pasajeros
    cercanos de forma automática.
    """

    def __init__(self, repo: Repositorio) -> None:
        self.repo = repo
        self._hilos: Dict[str, threading.Thread] = {}
        self._parar: Dict[str, bool] = {}

    def iniciar(self, conductor_id: str) -> None:
        if conductor_id in self._hilos:
            return

        self._parar[conductor_id] = False

        def bucle():
            while not self._parar[conductor_id]:
                c = self.repo.obtener_conductor(conductor_id)
                if not c or c.estado != EstadoConductor.ONLINE:
                    time.sleep(2)
                    continue

                # destino aleatorio
                ids_dest = self.repo.listar_ids_destinos()
                if not ids_dest:
                    time.sleep(5)
                    continue
                dest_id = random.choice(ids_dest)

                origen = dispersion_latlon(c.ubicacion, radio_metros=800)
                when = TIEMPO.ahora()
                precio = self.repo.cotizar(origen, dest_id, when)
                self.repo.crear_viaje(None, origen, dest_id, precio)
                time.sleep(5)  # cada 5s crea un potencial viaje

        t = threading.Thread(target=bucle, daemon=True)
        self._hilos[conductor_id] = t
        t.start()

    def detener(self, conductor_id: str) -> None:
        self._parar[conductor_id] = True
        self._hilos.pop(conductor_id, None)
