# backend/concurrencia/generador_auto_conductor.py
import threading
import random
from almacenamiento.repositorio import Repositorio
from dominio.geo import dispersion_latlon
from dominio.tiempo_sim import TIEMPO
from dominio.modelos import EstadoConductor


class GeneradorAutoConductor:
    """
    Por cada conductor ONLINE, lanza un hilo que:
      - genera un origen aleatorio cerca del conductor
      - elige un destino fijo al azar de los 5
      - calcula precio y crea el viaje (PENDIENTE)
      - despierta al asignador
    """
    def __init__(self, repo: Repositorio):
        self.repo = repo
        self._hilos: dict[str, tuple[threading.Thread, threading.Event]] = {}

    def iniciar(self, conductor_id: str):
        if conductor_id in self._hilos:
            return
        stop = threading.Event()
        th = threading.Thread(target=self._loop, args=(conductor_id, stop), daemon=True)
        self._hilos[conductor_id] = (th, stop)
        th.start()

    def detener(self, conductor_id: str):
        if conductor_id in self._hilos:
            th, stop = self._hilos.pop(conductor_id)
            stop.set()

    def _loop(self, conductor_id: str, stop: threading.Event):
        cfg = self.repo.cfg
        radius = cfg["radio_pasajero_cerca_conductor_m"]
        mean_gap = cfg["intervalo_medio_solicitudes_s"]

        while not stop.wait(timeout=random.expovariate(1.0 / mean_gap)):
            c = self.repo.obtener_conductor(conductor_id)
            if not c or c.estado != EstadoConductor.ONLINE or not c.ubicacion:
                continue

            # 1) origen alrededor del conductor
            olat, olon = dispersion_latlon(c.ubicacion[0], c.ubicacion[1], radio_m=radius)

            # 2) destino al azar
            dest_id = random.choice(self.repo.listar_ids_destinos())

            # 3) precio/ETA
            when = TIEMPO.ahora()
            precio = self.repo.cotizar((olat, olon), dest_id, when)

            # 4) crear viaje y notificar
            vj = self.repo.crear_viaje(None, (olat, olon), dest_id, precio)
            if self.repo.asignador:
                self.repo.asignador.submit(vj.id)
