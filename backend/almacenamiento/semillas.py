# backend/almacenamiento/semillas.py
from backend.almacenamiento.repositorio import Repositorio
from backend.dominio.modelos import Conductor, EstadoConductor


def cargar_semillas() -> None:
    """
    Crea algún dato de demo si quieres. Ahora mismo es opcional.
    """
    repo = Repositorio.instancia()
    # Ejemplo: no metemos nada para no ensuciar tu simulación real.
    # Podrías crear conductores/pasajeros de prueba aquí.
    return
