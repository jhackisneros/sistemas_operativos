# backend/concurrencia/liquidacion.py
import threading
from datetime import date

from almacenamiento.repositorio import Repositorio
from almacenamiento.locks import lock_liquidacion

_stop_event = threading.Event()
_thread: threading.Thread | None = None


def _cerrar_dia(repo: Repositorio):
    """
    Cierre diario:
      - Por cada conductor: 20% empresa, 80% conductor
      - Resetea ganancias_diarias y agrega asiento al ledger
    """
    with lock_liquidacion:
        hoy = date.today()
        for cid, c in repo.conductores.items():
            total = float(c.ganancias_diarias)
            if total <= 0.0:
                c.ultima_liquidacion = hoy
                repo.conductores[cid] = c
                continue
            empresa = round(total * 0.20, 2)
            neto = round(total * 0.80, 2)

            c.balance += neto
            c.ganancias_diarias = 0.0
            c.ultima_liquidacion = hoy
            repo.conductores[cid] = c

            repo.agregar_asiento_ledger(
                conductor_id=cid,
                fecha=hoy,
                total_dia=total,
                empresa_20=empresa,
                conductor_80=neto,
            )
        print("[Liquidación] cierre diario ejecutado")


def _daemon(repo: Repositorio):
    dur = repo.cfg.get("duracion_dia_real_seg", 300)  # 5 minutos reales por default
    while not _stop_event.wait(timeout=dur):
        _cerrar_dia(repo)


def iniciar_daemon_liquidacion(repo: Repositorio):
    global _thread
    if _thread and _thread.is_alive():
        return
    _stop_event.clear()
    _thread = threading.Thread(target=_daemon, args=(repo,), daemon=True)
    _thread.start()


def detener_daemon_liquidacion():
    _stop_event.set()
