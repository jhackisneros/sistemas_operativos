# backend/rutas/conductor.py
from fastapi import APIRouter, HTTPException
from backend.almacenamiento.repositorio import Repositorio
from backend.dominio.modelos import Conductor, EstadoConductor, EstadoTaxi, EstadoViaje
from backend.dominio.reglas import aprobar_o_rechazar_conductor
from backend.concurrencia.generador_auto_conductor import GeneradorAutoConductor

router = APIRouter()
repo = Repositorio.instancia()
spawner = GeneradorAutoConductor(repo)

@router.post("/registrar")
def registrar(
    conductor_id: str,
    nombre: str,
    licencia_ok: bool,
    antecedentes_ok: bool,
    placa: str,
    marca: str,
    modelo: str,
    lat: float,
    lon: float,
):
    c = Conductor(
        id=conductor_id,
        nombre=nombre,
        licencia_ok=licencia_ok,
        antecedentes_ok=antecedentes_ok,
        estado=EstadoConductor.PENDIENTE,
        ubicacion=(lat, lon),
    )
    c = aprobar_o_rechazar_conductor(c)
    repo.guardar_conductor(c)

    if c.estado == EstadoConductor.RECHAZADO:
        return {"estado": "RECHAZADO", "motivo": "Antecedentes penales"}

    if c.estado == EstadoConductor.APROBADO:
        t = repo.registrar_taxi(conductor_id, placa, marca, modelo)
        return {"estado": "APROBADO", "taxi_id": t.id}

    return {"estado": "PENDIENTE"}

@router.post("/online")
def online(conductor_id: str, lat: float, lon: float):
    c = repo.obtener_conductor(conductor_id)
    if not c:
        raise HTTPException(404, "Conductor no encontrado")
    if c.estado != EstadoConductor.APROBADO or not c.antecedentes_ok:
        raise HTTPException(403, "No autorizado para ponerse ONLINE")

    repo.actualizar_ubicacion_conductor(conductor_id, (lat, lon))
    c.estado = EstadoConductor.ONLINE
    repo.guardar_conductor(c)

    t = repo.obtener_taxi_por_conductor(conductor_id)
    if not t:
        raise HTTPException(409, "Conductor sin taxi registrado")
    repo.actualizar_estado_taxi(t.id, EstadoTaxi.LIBRE, ubicacion=(lat, lon))

    spawner.iniciar(conductor_id)
    return {"estado": "ONLINE", "taxi_id": t.id}

@router.post("/offline")
def offline(conductor_id: str):
    c = repo.obtener_conductor(conductor_id)
    if not c:
        raise HTTPException(404, "Conductor no encontrado")

    c.estado = EstadoConductor.OFFLINE
    repo.guardar_conductor(c)

    t = repo.obtener_taxi_por_conductor(conductor_id)
    if t:
        repo.actualizar_estado_taxi(t.id, EstadoTaxi.FUERA)

    spawner.detener(conductor_id)
    return {"estado": "OFFLINE"}

@router.post("/iniciar/{viaje_id}")
def iniciar_viaje(viaje_id: str, conductor_id: str):
    v = repo.obtener_viaje(viaje_id)
    if not v:
        raise HTTPException(404, "Viaje no encontrado")
    t = repo.obtener_taxi_por_conductor(conductor_id)
    if not t or v.taxi_id != t.id:
        raise HTTPException(403, "Este viaje no está asignado a tu taxi")
    if v.estado != EstadoViaje.ASIGNADO:
        raise HTTPException(409, "El viaje no está en estado ASIGNADO")
    repo.marcar_inicio_viaje(viaje_id)
    return {"ok": True, "estado": "EN_CURSO"}

@router.post("/finalizar/{viaje_id}")
def finalizar_viaje(viaje_id: str, conductor_id: str):
    v = repo.obtener_viaje(viaje_id)
    if not v:
        raise HTTPException(404, "Viaje no encontrado")
    t = repo.obtener_taxi_por_conductor(conductor_id)
    if not t or v.taxi_id != t.id:
        raise HTTPException(403, "Este viaje no está asignado a tu taxi")
    if v.estado != EstadoViaje.EN_CURSO:
        raise HTTPException(409, "El viaje no está en curso")
    repo.marcar_fin_viaje(viaje_id)
    return {"ok": True, "estado": "FINALIZADO", "monto": v.precio}
