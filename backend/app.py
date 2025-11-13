# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Rutas HTTP
from backend.rutas import comunes, pasajero, conductor, admin
# Rutas WebSocket
from backend.eventos import ws as eventos_ws

# Concurrencia (monitores/daemons)
from backend.concurrencia.asignador import iniciar_asignador
from backend.concurrencia.liquidacion import (
    iniciar_daemon_liquidacion,
    detener_daemon_liquidacion,
)

# Estado compartido / “BD” en memoria
from backend.almacenamiento.repositorio import Repositorio
from backend.almacenamiento.semillas import cargar_semillas


def crear_app() -> FastAPI:
    app = FastAPI(
        title="UNIETAXI",
        version="1.0.0",
        description="Backend de simulación UNIETAXI (concurrencia + liquidación acelerada)",
    )

    # CORS (ajusta allow_origins en producción)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Repositorio singleton
    repo = Repositorio.instancia()

    # Registrar routers HTTP
    app.include_router(comunes.router,   prefix="/comunes",   tags=["comunes"])
    app.include_router(pasajero.router,  prefix="/pasajero",  tags=["pasajero"])
    app.include_router(conductor.router, prefix="/conductor", tags=["conductor"])
    app.include_router(admin.router,     prefix="/admin",     tags=["admin"])
    # Registrar router WebSocket
    app.include_router(eventos_ws.router, tags=["websocket"])

    @app.on_event("startup")
    def _startup():
        # Cargar catálogos y configuración
        repo.cargar_destinos()
        repo.cargar_config()
        # Semillas de demo (opcional)
        try:
            cargar_semillas()
        except Exception as e:
            print("[Semillas] Aviso: no se pudieron cargar las semillas:", e)

        # Iniciar monitor de asignación (dispatcher)
        iniciar_asignador(repo)

        # Iniciar daemon de liquidación (cada 5 min reales = 24h simuladas)
        iniciar_daemon_liquidacion(repo)

    @app.on_event("shutdown")
    def _shutdown():
        # Detener daemon de liquidación
        detener_daemon_liquidacion()

    # Endpoints de salud
    @app.get("/", tags=["salud"])
    def raiz():
        return {"ok": True, "servicio": "UNIETAXI", "version": "1.0.0"}

    @app.get("/salud", tags=["salud"])
    def salud():
        return {"status": "UP"}

    return app


# Instancia para Uvicorn: `uvicorn backend.app:app --reload`
app = crear_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
