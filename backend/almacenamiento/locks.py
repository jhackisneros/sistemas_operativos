# backend/almacenamiento/locks.py
import threading
from collections import defaultdict

# Locks globales
lock_solicitudes = threading.Lock()
lock_taxis = threading.Lock()
lock_liquidacion = threading.Lock()

# Locks por entidad
lock_conductor = defaultdict(threading.Lock)  # lock_conductor[id_conductor]
lock_viaje = defaultdict(threading.Lock)      # lock_viaje[id_viaje]
