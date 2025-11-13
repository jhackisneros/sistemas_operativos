# backend/rutas/comunes.py
from fastapi import APIRouter, Query
from backend.almacenamiento.repositorio import Repositorio
from backend.dominio.tiempo_sim import TIEMPO

router = APIRouter()
repo = Repositorio.instancia()


@router.get("/destinos")
def destinos():
    return repo.listar_destinos()


@router.post("/tarifa")
def tarifa(
    lat: float = Query(...),
    lon: float = Query(...),
    dest_id: str = Query(...),
):
    if dest_id not in repo.destinos:
        return {"error": "destino_no_valido"}
    when = TIEMPO.ahora()
    precio = repo.cotizar((lat, lon), dest_id, when)
    eta = repo.estimar_eta_min((lat, lon), dest_id)
    return {"precio": precio, "eta_min": eta, "momento_sim": when.isoformat()}
