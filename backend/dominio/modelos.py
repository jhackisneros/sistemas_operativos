# backend/dominio/modelos.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple
from datetime import datetime, date
import uuid


class EstadoTaxi(str, Enum):
    LIBRE = "LIBRE"
    ASIGNADO = "ASIGNADO"
    EN_SERVICIO = "EN_SERVICIO"
    FUERA = "FUERA"


class EstadoViaje(str, Enum):
    PENDIENTE = "PENDIENTE"
    ASIGNADO = "ASIGNADO"
    EN_CURSO = "EN_CURSO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"


class EstadoConductor(str, Enum):
    PENDIENTE = "PENDIENTE"
    RECHAZADO = "RECHAZADO"
    APROBADO = "APROBADO"
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"


@dataclass
class Conductor:
    id: str
    nombre: str
    licencia_ok: bool = False
    antecedentes_ok: bool = True
    estado: EstadoConductor = EstadoConductor.PENDIENTE
    ubicacion: Optional[Tuple[float, float]] = None
    rating: float = 4.5
    ganancias_diarias: float = 0.0
    balance: float = 0.0
    ultima_liquidacion: Optional[date] = None


@dataclass
class Taxi:
    id: str
    conductor_id: str
    placa: str
    marca: str
    modelo: str
    estado: EstadoTaxi = EstadoTaxi.FUERA
    ubicacion: Optional[Tuple[float, float]] = None
    rating: float = 4.5


@dataclass
class Pasajero:
    id: str
    nombre: str


@dataclass
class Viaje:
    id: str
    pasajero_id: Optional[str]
    taxi_id: Optional[str]
    origen: Tuple[float, float]
    destino_id: str
    precio: float = 0.0
    estado: EstadoViaje = EstadoViaje.PENDIENTE
    creado_en: datetime = field(default_factory=datetime.utcnow)
    asignado_en: Optional[datetime] = None
    iniciado_en: Optional[datetime] = None
    finalizado_en: Optional[datetime] = None


def nuevo_id() -> str:
    return uuid.uuid4().hex
