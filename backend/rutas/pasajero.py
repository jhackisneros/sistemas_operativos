# backend/rutas/pasajero.py
from fastapi import APIRouter, HTTPException
import random
from almacenamiento.repositorio import Repositorio
from dominio.tiempo_sim import TIEMPO

router = APIRouter()
repo = Repositorio.instancia()

def _punto_aleatorio_bbox():
    b = repo.cfg["bbox_madrid"]
    lat = random.uniform(b["lat_min"], b["lat_max"])
    lon = random.uniform(b["lon_min"], b["lon_max"])
    return lat, lon

@router.post("/cotizar")
def cotizar(lat: float, lon: float, dest_id: str):
    """
    Devuelve precio + ETA sin crear viaje.
    """
    if dest_id not in repo.destinos:
        raise HTTPException(404, "Destino no válido")
    when = TIEMPO.ahora()
    precio = repo.cotizar((lat, lon), dest_id, when)
    eta = repo.estimar_eta_min((lat, lon), dest_id)
    return {"precio": precio, "eta_min": eta, "momento_sim": when.isoformat()}

@router.post("/solicitar")
def solicitar(pasajero_id: str, lat: float, lon: float, dest_id: str):
    """
    Crea la solicitud de viaje y la envía al asignador.
    Devuelve el ID de viaje (con el que el frontend abre el WebSocket /ws/pasajero/{viaje_id}).
    """
    if dest_id not in repo.destinos:
        raise HTTPException(404, "Destino no válido")
    when = TIEMPO.ahora()
    precio = repo.cotizar((lat, lon), dest_id, when)
    vj = repo.crear_viaje(pasajero_id, (lat, lon), dest_id, precio)
    # Despertar asignador
    if repo.asignador:
        repo.asignador.submit(vj.id)
    return {"viaje_id": vj.id, "precio": precio}

@router.post("/simular_aleatorio")
def simular_aleatorio(pasajero_id: str, dest_id: str):
    """
    Igual que /solicitar pero colocando al pasajero en un punto aleatorio del BBox de Madrid.
    """
    lat, lon = _punto_aleatorio_bbox()
    return solicitar(pasajero_id, lat, lon, dest_id)
