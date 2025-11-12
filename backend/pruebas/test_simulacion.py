# backend/pruebas/test_simulacion.py
import time
from datetime import datetime
from almacenamiento.repositorio import Repositorio
from concurrencia.asignador import iniciar_asignador
from concurrencia.generador_auto_conductor import GeneradorAutoConductor
from dominio.modelos import Conductor, EstadoConductor, EstadoTaxi

def _setup_repo():
    repo = Repositorio.instancia()
    try:
        repo.cargar_destinos()
        repo.cargar_config()
    except Exception:
        pass
    return repo

def test_generador_auto_crea_solicitudes_y_asigna():
    repo = _setup_repo()
    iniciar_asignador(repo)

    # Un conductor aprobado ONLINE con taxi LIBRE
    c = Conductor(id="c-sim", nombre="Sim", licencia_ok=True, antecedentes_ok=True, estado=EstadoConductor.APROBADO, ubicacion=(40.45,-3.69))
    repo.guardar_conductor(c)
    t = repo.registrar_taxi(c.id, "SIM111", "Opel", "Corsa")
    repo.actualizar_estado_taxi(t.id, EstadoTaxi.LIBRE, ubicacion=c.ubicacion)

    # Arranca spawner
    sp = GeneradorAutoConductor(repo)
    # Fuerza parámetros de prueba (más rápido)
    repo.cfg["intervalo_medio_solicitudes_s"] = 1
    repo.cfg["radio_pasajero_cerca_conductor_m"] = 200
    c.estado = EstadoConductor.ONLINE
    repo.guardar_conductor(c)
    sp.iniciar(c.id)

    # Espera a que aparezca y se asigne al menos 1 viaje
    asignado = False
    for _ in range(100):
        # ¿hay viaje ASIGNADO a t.id?
        viajes = [v for v in repo.viajes.values() if v.taxi_id == t.id]
        if viajes:
            asignado = True
            break
        time.sleep(0.05)

    # detener hilo
    sp.detener(c.id)

    assert asignado, "El generador automático debería crear y asignar al menos un viaje"
