# backend/concurrencia/liquidacion.py
import threading
import time
from datetime import date

from backend.almacenamiento.repositorio import Repositorio
from backend.almacenamiento.locks import lock_liquidacion

_daemon_hilo: threading.Thread | None = None
_detener = threading.Event()


def _cerrar_dia(repo: Repositorio) -> None:
    """
    Recorre conductores, aplica 20/80 y resetea ganancias_diarias.
    """
    hoy = date.today()
    with lock_liquidacion:
        for c in repo.conductores.values():
            total = c.ganancias_diarias
            if total <= 0:
                continue
            empresa_20 = total * 0.20
            conductor_80 = total * 0.80
            repo.agregar_asiento_ledger(c.id, hoy, total, empresa_20, conductor_80)
            c.ganancias_diarias = 0.0
            repo.conductores[c.id] = c


def _daemon(repo: Repositorio, intervalo_seg: float = 300.0) -> None:
    while not _detener.is_set():
        _cerrar_dia(repo)
        time.sleep(intervalo_seg)


def iniciar_daemon_liquidacion(repo: Repositorio) -> None:
    global _daemon_hilo
    if _daemon_hilo is not None:
        return
    # para desarrollo, podemos hacer más rápido: cada 30s
    intervalo = 300.0  # 5 min reales
    t = threading.Thread(target=_daemon, args=(repo, intervalo), daemon=True)
    _daemon_hilo = t
    t.start()


def detener_daemon_liquidacion() -> None:
    _detener.set()
