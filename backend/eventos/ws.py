# backend/eventos/ws.py
"""
WebSockets para actualizaciones en tiempo real.
Tópicos:
  - viaje.{viaje_id}         → eventos del viaje (estado, taxi asignado, ETA, etc.)
  - conductor.{conductor_id}  → eventos para el conductor (nuevas asignaciones, cambios)
Helpers:
  - publicar_evento_viaje(repo, viaje_id)
  - publicar_evento_conductor(repo, conductor_id)
Integra estos helpers en tu flujo (asignación, inicio/fin de viaje, online/offline).
"""

import json
import asyncio
from typing import Any, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from almacenamiento.repositorio import Repositorio
from dominio.modelos import EstadoViaje, EstadoTaxi, Viaje
from dominio.geo import haversine_km
from .bus import BUS

router = APIRouter()
repo = Repositorio.instancia()


# -------------------- Helpers para publicar eventos --------------------

async def publicar_evento_viaje(viaje: Viaje) -> None:
    """
    Publica el snapshot del viaje al tópico 'viaje.{id}'.
    """
    payload = {
        "tipo": "VIAJE_UPDATE",
        "viaje": {
            "id": viaje.id,
            "pasajero_id": viaje.pasajero_id,
            "taxi_id": viaje.taxi_id,
            "origen": {"lat": viaje.origen[0], "lon": viaje.origen[1]},
            "destino_id": viaje.destino_id,
            "precio": viaje.precio,
            "estado": viaje.estado,
            "creado_en": viaje.creado_en.isoformat(),
            "asignado_en": viaje.asignado_en.isoformat() if viaje.asignado_en else None,
            "iniciado_en": viaje.iniciado_en.isoformat() if viaje.iniciado_en else None,
            "finalizado_en": viaje.finalizado_en.isoformat() if viaje.finalizado_en else None,
        }
    }
    await BUS.publish(f"viaje.{viaje.id}", payload)


async def publicar_evento_conductor(conductor_id: str, data: Dict[str, Any]) -> None:
    """
    Publica un evento genérico para el conductor.
    """
    payload = {"tipo": "CONDUCTOR_EVENT", **data}
    await BUS.publish(f"conductor.{conductor_id}", payload)


# Helpers opcionales para llamadas rápidas desde otros módulos
async def notificar_asignacion(viaje_id: str) -> None:
    v = repo.obtener_viaje(viaje_id)
    if v:
        await publicar_evento_viaje(v)
        if v.taxi_id:
            taxi = repo.taxis.get(v.taxi_id)
            if taxi:
                await publicar_evento_conductor(taxi.conductor_id, {
                    "evento": "ASIGNACION",
                    "viaje_id": v.id,
                    "destino_id": v.destino_id
                })


async def notificar_inicio(viaje_id: str) -> None:
    v = repo.obtener_viaje(viaje_id)
    if v:
        await publicar_evento_viaje(v)


async def notificar_finalizacion(viaje_id: str) -> None:
    v = repo.obtener_viaje(viaje_id)
    if v:
        await publicar_evento_viaje(v)
        if v.taxi_id:
            taxi = repo.taxis.get(v.taxi_id)
            if taxi:
                await publicar_evento_conductor(taxi.conductor_id, {
                    "evento": "VIAJE_FINALIZADO",
                    "viaje_id": v.id,
                    "monto": v.precio
                })


# -------------------- Endpoints WebSocket --------------------

@router.websocket("/ws/pasajero/{viaje_id}")
async def ws_pasajero(websocket: WebSocket, viaje_id: str):
    """
    El pasajero se conecta a su canal de viaje para recibir actualizaciones.
    """
    await websocket.accept()
    topic = f"viaje.{viaje_id}"
    queue = await BUS.subscribe(topic)

    # Enviar un snapshot inicial si existe
    v = repo.obtener_viaje(viaje_id)
    if v:
        try:
            await websocket.send_text(json.dumps({
                "tipo": "SNAPSHOT",
                "viaje_id": viaje_id,
                "estado": v.estado,
                "taxi_id": v.taxi_id,
                "precio": v.precio
            }))
        except Exception:
            pass

    try:
        while True:
            # Espera evento del bus o ping del cliente
            done, pending = await asyncio.wait(
                [queue.get(), websocket.receive_text()],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in done:
                result = task.result()
                # Si viene del cliente, puede ser ping/keepalive
                if isinstance(result, str):
                    # opcional: interpretar comandos del cliente
                    if result == "ping":
                        await websocket.send_text("pong")
                else:
                    # viene del bus (dict serializable)
                    await websocket.send_text(json.dumps(result))

            # Cancelar pendientes para el siguiente ciclo
            for p in pending:
                p.cancel()

    except WebSocketDisconnect:
        pass
    except Exception:
        # Cierra silenciosamente
        pass
    finally:
        await BUS.unsubscribe(topic, queue)
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)


@router.websocket("/ws/conductor/{conductor_id}")
async def ws_conductor(websocket: WebSocket, conductor_id: str):
    """
    El conductor se conecta a su canal para recibir asignaciones y eventos.
    """
    await websocket.accept()
    topic = f"conductor.{conductor_id}"
    queue = await BUS.subscribe(topic)

    # Opcional: enviar estado inicial del taxi asociado
    taxi = repo.obtener_taxi_por_conductor(conductor_id)
    if taxi:
        try:
            await websocket.send_text(json.dumps({
                "tipo": "SNAPSHOT",
                "conductor_id": conductor_id,
                "taxi_id": taxi.id,
                "estado_taxi": taxi.estado,
                "ubicacion": taxi.ubicacion,
            }))
        except Exception:
            pass

    try:
        while True:
            done, pending = await asyncio.wait(
                [queue.get(), websocket.receive_text()],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in done:
                result = task.result()
                if isinstance(result, str):
                    if result == "ping":
                        await websocket.send_text("pong")
                else:
                    await websocket.send_text(json.dumps(result))

            for p in pending:
                p.cancel()

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        await BUS.unsubscribe(topic, queue)
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
