# backend/eventos/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from backend.almacenamiento.repositorio import Repositorio
from backend.dominio.modelos import EstadoViaje, EstadoTaxi

router = APIRouter()
repo = Repositorio.instancia()


@router.websocket("/ws/pasajero/{viaje_id}")
async def ws_pasajero(websocket: WebSocket, viaje_id: str):
    await websocket.accept()
    try:
        while True:
            v = repo.obtener_viaje(viaje_id)
            if not v:
                await websocket.send_json({"error": "viaje_no_encontrado"})
                await asyncio.sleep(1)
                continue

            taxi_info = None
            if v.taxi_id and v.taxi_id in repo.taxis:
                taxi = repo.taxis[v.taxi_id]
                taxi_info = {
                    "id": taxi.id,
                    "ubicacion": taxi.ubicacion,
                    "estado": taxi.estado.name,
                    "rating": taxi.rating,
                }

            await websocket.send_json(
                {
                    "viaje": {
                        "id": v.id,
                        "estado": v.estado.name,
                        "precio": v.precio,
                        "destino_id": v.destino_id,
                    },
                    "taxi": taxi_info,
                }
            )
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        return
