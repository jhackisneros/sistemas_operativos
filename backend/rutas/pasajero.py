# backend/rutas/pasajero.py
from fastapi import APIRouter, HTTPException
import random
from backend.almacenamiento.repositorio import Repositorio
from backend.dominio.tiempo_sim import TIEMPO

router = APIRouter()
repo = Repositorio.instancia()


def _punto_aleatorio_bbox():
    b = repo.cfg["bbox_madrid"]
    lat = random.uniform(b["lat_min"], b["lat_max"])
    lon = random.uniform(b["lon_min"], b["lon_max"])
    return lat, lon


@router.post("/cotizar")
def cotizar(lat: float, lon: float, dest_id: str):
    if dest_id not in repo.destinos:
        raise HTTPException(404, "Destino no válido")
    when = TIEMPO.ahora()
    precio = repo.cotizar((lat, lon), dest_id, when)
    eta = repo.estimar_eta_min((lat, lon), dest_id)
    return {"precio": precio, "eta_min": eta, "momento_sim": when.isoformat()}


@router.post("/solicitar")
def solicitar(pasajero_id: str, lat: float, lon: float, dest_id: str):
    if dest_id not in repo.destinos:
        raise HTTPException(404, "Destino no válido")
    when = TIEMPO.ahora()
    precio = repo.cotizar((lat, lon), dest_id, when)
    vj = repo.crear_viaje(pasajero_id, (lat, lon), dest_id, precio)
    if repo.asignador:
        repo.asignador.repo.push_solicitud(vj.id)
    return {"viaje_id": vj.id, "precio": precio}


@router.post("/simular_aleatorio")
def simular_aleatorio(pasajero_id: str, dest_id: str):
    lat, lon = _punto_aleatorio_bbox()
    return solicitar(pasajero_id, lat, lon, dest_id)


@router.post("/calificar")
def calificar(viaje_id: str, puntuacion: int, comentario: str = ""):
    v = repo.obtener_viaje(viaje_id)
    if not v:
        raise HTTPException(404, "Viaje no encontrado")
    # Aquí podrías acumular rating al conductor, etc.
    # De momento solo devolvemos el payload.
    return {
        "ok": True,
        "viaje_id": viaje_id,
        "puntuacion": puntuacion,
        "comentario": comentario,
    }
