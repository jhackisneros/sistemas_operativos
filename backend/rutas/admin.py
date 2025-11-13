# backend/rutas/admin.py
from fastapi import APIRouter
from datetime import date
from backend.almacenamiento.repositorio import Repositorio
from backend.concurrencia.liquidacion import _cerrar_dia

router = APIRouter()
repo = Repositorio.instancia()

@router.post("/cierre_dia")
def cierre_manual():
    _cerrar_dia(repo)
    return {"ok": True}

@router.get("/liquidaciones/{yyyy}-{mm}-{dd}")
def liquidaciones_por_fecha(yyyy: int, mm: int, dd: int):
    fecha = date(yyyy, mm, dd)
    return repo.listar_liquidaciones_por_fecha(fecha)
