# backend/pruebas/test_asignador.py
import time
from datetime import datetime
from almacenamiento.repositorio import Repositorio
from concurrencia.asignador import iniciar_asignador
from dominio.modelos import Conductor, EstadoConductor, EstadoTaxi, Viaje

def _setup_repo():
    repo = Repositorio.instancia()
    try:
        repo.cargar_destinos()
        repo.cargar_config()
    except Exception:
        pass
    return repo

def test_asignador_asigna_taxi_mas_cercano():
    repo = _setup_repo()
    iniciar_asignador(repo)

    # Dos conductores aprobados con sus taxis
    c1 = Conductor(id="c-a1", nombre="A1", licencia_ok=True, antecedentes_ok=True, estado=EstadoConductor.APROBADO, ubicacion=(40.45,-3.69))
    c2 = Conductor(id="c-b1", nombre="B1", licencia_ok=True, antecedentes_ok=True, estado=EstadoConductor.APROBADO, ubicacion=(40.40,-3.70))
    repo.guardar_conductor(c1); repo.guardar_conductor(c2)
    t1 = repo.registrar_taxi("c-a1", "AAA111", "Seat", "Leon")
    t2 = repo.registrar_taxi("c-b1", "BBB222", "VW", "Polo")

    # Ambos ONLINE/LIBRE
    repo.actualizar_estado_taxi(t1.id, EstadoTaxi.LIBRE, ubicacion=c1.ubicacion)
    repo.actualizar_estado_taxi(t2.id, EstadoTaxi.LIBRE, ubicacion=c2.ubicacion)

    # Solicitud cerca de c1 (más cercano)
    origen = (40.451, -3.689)   # pegado a c1
    precio = repo.cotizar(origen, "RET", datetime(2025,1,1,12,0,0))
    vj: Viaje = repo.crear_viaje("p-x", origen, "RET", precio)

    # Despertar asignador
    repo.asignador.submit(vj.id)

    # Espera breve a que el hilo asigne
    for _ in range(30):
        v = repo.obtener_viaje(vj.id)
        if v and v.taxi_id:
            break
        time.sleep(0.05)

    v = repo.obtener_viaje(vj.id)
    assert v.taxi_id == t1.id, "Debe asignar el taxi más cercano"
