# backend/almacenamiento/semillas.py
from dominio.modelos import Conductor, Pasajero, EstadoConductor
from .repositorio import Repositorio

def cargar_semillas() -> None:
    repo = Repositorio.instancia()

    # Pasajeros demo
    p1 = Pasajero(id="p-demo-1", nombre="Alicia")
    p2 = Pasajero(id="p-demo-2", nombre="Bruno")
    repo.pasajeros[p1.id] = p1
    repo.pasajeros[p2.id] = p2

    # Conductores demo
    c1 = Conductor(id="c-demo-1", nombre="Carlos", licencia_ok=True, antecedentes_ok=True, estado=EstadoConductor.APROBADO)
    c2 = Conductor(id="c-demo-2", nombre="Diana",  licencia_ok=True, antecedentes_ok=True, estado=EstadoConductor.APROBADO)
    repo.conductores[c1.id] = c1
    repo.conductores[c2.id] = c2

    # (El registro de taxi se hace desde rutas/conductor al aprobar/online)
    print("[Semillas] Cargadas entidades demo (2 pasajeros, 2 conductores).")
