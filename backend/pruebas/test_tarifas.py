# backend/pruebas/test_tarifas.py
from datetime import datetime
from almacenamiento.repositorio import Repositorio

def _setup_repo():
    repo = Repositorio.instancia()
    # Carga única en todo el set de tests (si ya cargó, no pasa nada)
    try:
        repo.cargar_destinos()
        repo.cargar_config()
    except Exception:
        pass
    return repo

def test_tarifa_minima_y_por_km():
    repo = _setup_repo()
    # origen muy cercano a T4 para no superar demasiado el mínimo
    origen = (40.4922, -3.5932)  # casi T4
    precio = repo.cotizar(origen, "T4", datetime(2025, 1, 1, 10, 0, 0))
    # mínimo es 5.0; con suplemento T4 (+5) debería ser >= 10
    assert precio >= 10.0

def test_suplemento_nocturno_y_T4():
    repo = _setup_repo()
    origen = (40.45, -3.69)  # zona centro-norte Madrid
    p_dia = repo.cotizar(origen, "T4", datetime(2025, 1, 1, 12, 0, 0))   # sin nocturno
    p_noc = repo.cotizar(origen, "T4", datetime(2025, 1, 1, 23, 30, 0))  # nocturno 22–06
    # nocturno agrega 2 €, T4 agrega 5 €, así que p_noc >= p_dia + 2
    assert p_noc >= p_dia + 2.0
