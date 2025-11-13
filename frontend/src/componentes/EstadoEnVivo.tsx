// frontend/src/componentes/EstadoEnVivo.tsx
import { useEffect, useState } from "react";

type Props = {
  viajeId: string;
};

export default function EstadoEnVivo({ viajeId }: Props) {
  const [mensajes, setMensajes] = useState<string[]>([]);
  const [estado, setEstado] = useState<string>("CONECTANDO...");

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/pasajero/${viajeId}`);

    ws.onopen = () => {
      setEstado("Conectado");
      ws.send("ping");
    };

    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        setMensajes((prev) => [
          `${new Date().toLocaleTimeString()} → ${ev.data}`,
          ...prev,
        ]);
        if (data.viaje && data.viaje.estado) {
          setEstado(`Estado viaje: ${data.viaje.estado}`);
        }
      } catch {
        setMensajes((prev) => [
          `${new Date().toLocaleTimeString()} → ${ev.data}`,
          ...prev,
        ]);
      }
    };

    ws.onerror = () => setEstado("Error en WebSocket");
    ws.onclose = () => setEstado("Desconectado");

    return () => {
      ws.close();
    };
  }, [viajeId]);

  return (
    <div className="estado-envivo">
      <h3>Estado en vivo</h3>
      <p>{estado}</p>
      <div className="log">
        {mensajes.map((m, i) => (
          <pre key={i}>{m}</pre>
        ))}
      </div>
    </div>
  );
}
