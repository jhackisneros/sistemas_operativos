# backend/eventos/bus.py
"""
Bus de eventos muy simple (pub/sub) en memoria, basado en asyncio.
Cada suscriptor recibe un asyncio.Queue con los mensajes del tópico al que se suscribe.
"""

import asyncio
from typing import Any, Dict, Set


class EventBus:
    def __init__(self) -> None:
        # tópico -> conjunto de colas (suscriptores)
        self._topics: Dict[str, Set[asyncio.Queue]] = {}
        self._lock = asyncio.Lock()

    async def publish(self, topic: str, message: Any) -> None:
        """Publica un mensaje en 'topic' para todos los suscriptores actuales."""
        async with self._lock:
            queues = list(self._topics.get(topic, set()))
        # fuera del lock para no bloquear a productores
        for q in queues:
            # No usar put_nowait para no perder backpressure; con try/except por si se cerró
            try:
                await q.put(message)
            except Exception:
                pass

    async def subscribe(self, topic: str) -> asyncio.Queue:
        """Crea una nueva cola suscrita al 'topic' y la devuelve."""
        q: asyncio.Queue = asyncio.Queue(maxsize=100)
        async with self._lock:
            if topic not in self._topics:
                self._topics[topic] = set()
            self._topics[topic].add(q)
        return q

    async def unsubscribe(self, topic: str, queue: asyncio.Queue) -> None:
        """Elimina una cola del conjunto de suscriptores del tópico."""
        async with self._lock:
            if topic in self._topics and queue in self._topics[topic]:
                self._topics[topic].remove(queue)
                if not self._topics[topic]:
                    del self._topics[topic]
        # drena/cierra la cola
        try:
            while not queue.empty():
                queue.get_nowait()
        except Exception:
            pass


# Instancia global para usar en todo el backend
BUS = EventBus()
