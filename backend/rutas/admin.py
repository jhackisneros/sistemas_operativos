# backend/rutas/admin.py
from fastapi import APIRouter
from datetime import date
from almacenamiento.repositorio import Repositorio
from concurrencia.liquidacion import _cerrar_dia

router = APIRouter()
repo = Repositorio.instancia()

@router.post("/cierre_dia")
def cierre_manual():
    """
    Ejecuta el cierre contable inmediatamente (20% empresa / 80% conductor).
    Útil para pruebas (normalmente lo hace el daemon cada ~5 min reales).
    """
    _cerrar_dia(repo)
    return {"ok": True}

@router.get("/liquidaciones/{yyyy}-{mm}-{dd}")
def liquidaciones_por_fecha(yyyy: int, mm: int, dd: int):
    """
    Devuelve los asientos de liquidación para una fecha concreta.
    """
    fecha = date(yyyy, mm, dd)
    return repo.listar_liquidaciones_por_fecha(fecha)
