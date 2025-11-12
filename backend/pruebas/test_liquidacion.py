# backend/pruebas/test_liquidacion.py
from datetime import date
from almacenamiento.repositorio import Repositorio
from concurrencia.liquidacion import _cerrar_dia
from dominio.modelos import Conductor, EstadoConductor

def _setup_repo():
    repo = Repositorio.instancia()
    try:
        repo.cargar_destinos()
        repo.cargar_config()
    except Exception:
        pass
    return repo

def test_liquidacion_20_80_resetea_ganancias_y_agrega_ledger():
    repo = _setup_repo()

    c = Conductor(id="c-liq", nombre="Liq", licencia_ok=True, antecedentes_ok=True, estado=EstadoConductor.APROBADO)
    repo.guardar_conductor(c)
    # simula dinero ganado en el día
    repo.conductores[c.id].ganancias_diarias = 100.0

    _cerrar_dia(repo)

    c2 = repo.obtener_conductor(c.id)
    assert c2.ganancias_diarias == 0.0
    # 80 al conductor
    assert c2.balance >= 80.0 - 1e-6

    hoy = date.today().isoformat()
    asientos = repo.listar_liquidaciones_por_fecha(date.today())
    assert any(a["conductor_id"] == c.id and a["fecha"] == hoy for a in asientos)
    