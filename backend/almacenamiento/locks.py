# backend/almacenamiento/locks.py
from threading import RLock
from collections import defaultdict

# Locks globales
lock_solicitudes = RLock()   # protege cola_solicitudes
lock_taxis       = RLock()   # protege estado/ubicación de taxis
lock_liquidacion = RLock()   # protege proceso de cierre diario y ledger

# Locks por entidad (se crean bajo demanda)
lock_conductor = defaultdict(RLock)  # clave = conductor_id
lock_viaje     = defaultdict(RLock)  # clave = viaje_id
