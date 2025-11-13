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
    _inst: "Repositorio" | None = None

    @classmethod
    def instancia(cls) -> "Repositorio":
        if not cls._inst:
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

        self.asignador = None  # se inyecta desde concurrencia.asignador

    # ---------- catálogos ----------
    def cargar_destinos(self) -> None:
        ruta = os.path.join("backend", "almacenamiento", "destinos.json")
        if not os.path.exists(ruta):
            print("[destinos] No se encontró destinos.json, se usará solo la lista fija en frontend.")
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
            # valores por defecto
            self.cfg = {
                "tarifa_base": 3.0,
                "precio_km": 1.2,
                "suplemento_nocturno": 1.0,
                "suplemento_t4": 5.0,
                "velocidad_kmh": 25.0,
                "bbox_madrid": {
                    "lat_min": 40.35,
                    "lat_max": 40.50,
                    "lon_min": -3.80,
                    "lon_max": -3.55,
                },
            }

    def listar_destinos(self) -> List[dict]:
        return list(self.destinos_info.values())

    def listar_ids_destinos(self) -> List[str]:
        return list(self.destinos.keys())

    # ---------- utilidades tarifa / ETA ----------
    def cotizar(self, origen: Tuple[float, float], destino_id: str, cuando: datetime) -> float:
        base = calcular_tarifa(origen, self.destinos[destino_id], self.cfg)
        s = aplicar_suplementos(destino_id, cuando, self.cfg, evento_ber=False)
        return round(base + s, 2)

    def estimar_eta_min(self, origen: Tuple[float, float], destino_id: str) -> float:
        km = haversine_km(origen, self.destinos[destino_id])
        v = self.cfg.get("velocidad_kmh", 25.0)
        return round((km / v) * 60, 1)

    # ---------- pasajeros ----------
    def crear_pasajero(self, nombre: str) -> Pasajero:
        p = Pasajero(id=nuevo_id(), nombre=nombre)
        self.pasajeros[p.id] = p
        return p

    # ---------- conductores ----------
    def guardar_conductor(self, c: Conductor) -> None:
        self.conductores[c.id] = c

    def obtener_conductor(self, conductor_id: str) -> Optional[Conductor]:
        return self.conductores.get(conductor_id)

    def actualizar_ubicacion_conductor(self, conductor_id: str, pos: Tuple[float, float]) -> None:
        c = self.conductores[conductor_id]
        c.ubicacion = pos
        self.conductores[conductor_id] = c

    # ---------- taxis ----------
    def registrar_taxi(self, conductor_id: str, placa: str, marca: str, modelo: str) -> Taxi:
        t = Taxi(
            id=nuevo_id(),
            conductor_id=conductor_id,
            placa=placa,
            marca=marca,
            modelo=modelo,
            estado=EstadoTaxi.FUERA,
            ubicacion=self.conductores[conductor_id].ubicacion,
            rating=4.5,
        )
        self.taxis[t.id] = t
        return t

    def obtener_taxi_por_conductor(self, conductor_id: str) -> Optional[Taxi]:
        for t in self.taxis.values():
            if t.conductor_id == conductor_id:
                return t
        return None

    def actualizar_estado_taxi(
        self,
        taxi_id: str,
        estado: EstadoTaxi,
        ubicacion: Tuple[float, float] | None = None
    ) -> None:
        with lock_taxis:
            t = self.taxis[taxi_id]
            t.estado = estado
            if ubicacion:
                t.ubicacion = ubicacion
            self.taxis[taxi_id] = t

    # ---------- viajes ----------
    def crear_viaje(
        self,
        pasajero_id: Optional[str],
        origen: Tuple[float, float],
        destino_id: str,
        precio: float
    ) -> Viaje:
        vj = Viaje(
            id=nuevo_id(),
            pasajero_id=pasajero_id,
            taxi_id=None,
            origen=origen,
            destino_id=destino_id,
            precio=precio,
            estado=EstadoViaje.PENDIENTE,
        )
        self.viajes[vj.id] = vj
        with lock_solicitudes:
            self.cola_solicitudes.append(vj.id)
        return vj

    def obtener_viaje(self, viaje_id: str) -> Optional[Viaje]:
        return self.viajes.get(viaje_id)

    def marcar_asignado(self, viaje_id: str, taxi_id: str, ts: datetime | None = None) -> None:
        with lock_viaje[viaje_id]:
            vj = self.viajes[viaje_id]
            vj.taxi_id = taxi_id
            vj.estado = EstadoViaje.ASIGNADO
            vj.asignado_en = ts or datetime.utcnow()
            self.viajes[viaje_id] = vj

    def marcar_inicio_viaje(self, viaje_id: str, ts: datetime | None = None) -> None:
        with lock_viaje[viaje_id]:
            vj = self.viajes[viaje_id]
            vj.estado = EstadoViaje.EN_CURSO
            vj.iniciado_en = ts or datetime.utcnow()
            self.viajes[viaje_id] = vj

    def marcar_fin_viaje(self, viaje_id: str, ts: datetime | None = None) -> None:
        with lock_viaje[viaje_id]:
            vj = self.viajes[viaje_id]
            vj.estado = EstadoViaje.FINALIZADO
            vj.finalizado_en = ts or datetime.utcnow()
            self.viajes[viaje_id] = vj

        if vj.taxi_id:
            taxi = self.taxis[vj.taxi_id]
            c = self.conductores[taxi.conductor_id]
            with lock_conductor[c.id]:
                c.ganancias_diarias += vj.precio
                self.conductores[c.id] = c

            self.actualizar_estado_taxi(taxi.id, EstadoTaxi.LIBRE)

    def listar_viajes_conductor(self, conductor_id: str) -> List[Viaje]:
        taxi = self.obtener_taxi_por_conductor(conductor_id)
        if not taxi:
            return []
        return [v for v in self.viajes.values() if v.taxi_id == taxi.id]

    def listar_viajes_pasajero(self, pasajero_id: str) -> List[Viaje]:
        return [v for v in self.viajes.values() if v.pasajero_id == pasajero_id]

    # ---------- cola solicitudes ----------
    def pop_solicitud(self) -> Optional[str]:
        with lock_solicitudes:
            if not self.cola_solicitudes:
                return None
            return self.cola_solicitudes.pop(0)

    def push_solicitud(self, viaje_id: str) -> None:
        with lock_solicitudes:
            self.cola_solicitudes.append(viaje_id)

    # ---------- ledger / liquidaciones ----------
    def agregar_asiento_ledger(
        self,
        conductor_id: str,
        fecha: date,
        total_dia: float,
        empresa_20: float,
        conductor_80: float
    ) -> None:
        asiento = {
            "conductor_id": conductor_id,
            "fecha": fecha.isoformat(),
            "total_dia": round(total_dia, 2),
            "empresa_20": round(empresa_20, 2),
            "conductor_80": round(conductor_80, 2),
        }
        with lock_liquidacion:
            self.ledger.append(asiento)

    def listar_liquidaciones_por_fecha(self, fecha: date) -> List[dict]:
        s = fecha.isoformat()
        return [a for a in self.ledger if a["fecha"] == s]
