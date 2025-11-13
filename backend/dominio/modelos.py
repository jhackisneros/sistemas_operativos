# backend/dominio/modelos.py
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple
from datetime import datetime
import uuid


def nuevo_id() -> str:
    return uuid.uuid4().hex[:12]


class EstadoConductor(Enum):
    PENDIENTE = auto()
    APROBADO = auto()
    RECHAZADO = auto()
    ONLINE = auto()
    OFFLINE = auto()


class EstadoTaxi(Enum):
    FUERA = auto()
    LIBRE = auto()
    OCUPADO = auto()


class EstadoViaje(Enum):
    PENDIENTE = auto()
    ASIGNADO = auto()
    EN_CURSO = auto()
    FINALIZADO = auto()
    CANCELADO = auto()


@dataclass
class Pasajero:
    id: str
    nombre: str


@dataclass
class Conductor:
    id: str
    nombre: str
    licencia_ok: bool
    antecedentes_ok: bool
    estado: EstadoConductor = EstadoConductor.PENDIENTE
    ubicacion: Tuple[float, float] = (40.4168, -3.7038)
    ganancias_diarias: float = 0.0
    rating: float = 4.5


@dataclass
class Taxi:
    id: str
    conductor_id: str
    placa: str
    marca: str
    modelo: str
    estado: EstadoTaxi
    ubicacion: Tuple[float, float]
    rating: float = 4.5


@dataclass
class Viaje:
    id: str
    pasajero_id: Optional[str]
    taxi_id: Optional[str]
    origen: Tuple[float, float]
    destino_id: str
    precio: float
    estado: EstadoViaje
    asignado_en: Optional[datetime] = None
    iniciado_en: Optional[datetime] = None
    finalizado_en: Optional[datetime] = None
