# backend/rutas/comunes.py
from fastapi import APIRouter, Query
from almacenamiento.repositorio import Repositorio
from dominio.tiempo_sim import TIEMPO

router = APIRouter()
repo = Repositorio.instancia()

@router.get("/destinos")
def destinos():
    """
    Lista de destinos fijos (5 lugares).
    """
    return repo.listar_destinos()

@router.get("/tarifa")
def tarifa(
    lat: float = Query(..., description="Latitud del origen"),
    lon: float = Query(..., description="Longitud del origen"),
    dest_id: str = Query(..., description="ID del destino fijo: RET|BER|CDC|MAT|T4"),
):
    """
    Cotización (precio y ETA) desde una coordenada al destino fijo.
    """
    when = TIEMPO.ahora()
    precio = repo.cotizar((lat, lon), dest_id, when)
    eta = repo.estimar_eta_min((lat, lon), dest_id)
    return {"precio": precio, "eta_min": eta, "momento_sim": when.isoformat()}
