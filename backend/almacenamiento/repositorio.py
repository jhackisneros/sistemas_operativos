# backend/almacenamiento/repositorio.py
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime, date
import os

from backend.almacenamiento.locks import (
    lock_solicitudes, lock_taxis, lock_liquidacion,
    lock_conductor, lock_viaje
)

from backend.dominio.modelos import (
    Conductor, Taxi, Pasajero, Viaje,
    EstadoConductor, EstadoTaxi, EstadoViaje,
    nuevo_id
)
from backend.dominio.geo import haversine_km
from backend.dominio.tarifas import calcular_tarifa, aplicar_suplementos


class Repositorio:
    # ESTA ES LA LÍNEA CORREGIDA
    _inst: None

    @classmethod
    def instancia(cls) -> "Repositorio":
        if cls._inst is None:
            cls._inst = Repositorio()
        return cls._inst

    def __init__(self) -> None:
        self.destinos: Dict[str, Tuple[float, float]] = {}
        self.destinos_info: Dict[str, dict] = {}
        self.cfg: dict = {}

        self.conductores: Dict[str, Conductor] = {}
        self.taxis: Dict[str, Taxi] = {}
        self.pasajeros: Dict[str, Pasajero] = {}
        self.viajes: Dict[str, Viaje] = {}

        self.cola_solicitudes: List[str] = []
        self.ledger: List[dict] = []

        self.asignador = None

    # ---------- entrada de catálogos ----------
    def cargar_destinos(self) -> None:
        ruta = os.path.join("backend", "almacenamiento", "destinos.json")
        if not os.path.exists(ruta):
            print("[destinos] No existe destinos.json.")
            return
        with open(ruta, "r", encoding="utf-8") as f:
            arr = json.load(f)
        for d in arr:
            self.destinos[d["id"]] = (d["lat"], d["lon"])
            self.destinos_info[d["id"]] = d

    def cargar_config(self) -> None:
        ruta = os.path.join("backend", "almacenamiento", "config.json")
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {
                "tarifa_base": 3.0,
                "precio_km": 1.2,
                "suplemento_nocturno": 1.0,
                "suplemento_t4": 5.0,
                "velocidad_kmh": 25.0
            }

    # ---------- destinos ----------
    def listar_destinos(self) -> List[dict]:
        return list(self.destinos_info.values())

    def listar_ids_destinos(self) -> List[str]:
        return list(self.destinos.keys())

    # ---------- utilidades ----------
    def cotizar(self, origen, destino_id, cuando):
        base = calcular_tarifa(origen, self.destinos[destino_id], self.cfg)
        sup = aplicar_suplementos(destino_id, cuando, self.cfg)
        return round(base + sup, 2)

    def estimar_eta_min(self, origen, destino_id):
        km = haversine_km(origen, self.destinos[destino_id])
        v = self.cfg.get("velocidad_kmh", 25.0)
        return round((km / v) * 60, 1)

    # ---------- pasajeros ----------
    def crear_pasajero(self, nombre):
        p = Pasajero(id=nuevo_id(), nombre=nombre)
        self.pasajeros[p.id] = p
        return p

    # ---------- conductores ----------
    def guardar_conductor(self, c):
        self.conductores[c.id] = c

    def obtener_conductor(self, conductor_id):
        return self.conductores.get(conductor_id)

    # ---------- taxis ----------
    def registrar_taxi(self, conductor_id, placa, marca, modelo):
        t = Taxi(
            id=nuevo_id(),
            conductor_id=conductor_id,
            placa=placa,
            marca=marca,
            modelo=modelo,
            estado=EstadoTaxi.FUERA,
            ubicacion=self.conductores[conductor_id].ubicacion,
            rating=4.5
        )
        self.taxis[t.id] = t
        return t

    def obtener_taxi_por_conductor(self, conductor_id):
        for t in self.taxis.values():
            if t.conductor_id == conductor_id:
                return t
        return None

    # ---------- viajes ----------
    def crear_viaje(self, pasajero_id, origen, destino_id, precio):
        v = Viaje(
            id=nuevo_id(),
            pasajero_id=pasajero_id,
            taxi_id=None,
            origen=origen,
            destino_id=destino_id,
            precio=precio,
            estado=EstadoViaje.PENDIENTE
        )
        self.viajes[v.id] = v

        with lock_solicitudes:
            self.cola_solicitudes.append(v.id)

        return v

    def obtener_viaje(self, viaje_id):
        return self.viajes.get(viaje_id)

    # ---------- ledger ----------
    def agregar_asiento_ledger(self, conductor_id, fecha, total, empresa20, conductor80):
        asiento = {
            "conductor_id": conductor_id,
            "fecha": fecha.isoformat(),
            "total_dia": round(total, 2),
            "empresa_20": round(empresa20, 2),
            "conductor_80": round(conductor80, 2)
        }
        with lock_liquidacion:
            self.ledger.append(asiento)

    def listar_liquidaciones_por_fecha(self, fecha):
        s = fecha.isoformat()
        return [a for a in self.ledger if a["fecha"] == s]
