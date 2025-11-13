// frontend/src/paginas/pasajero/Solicitud.tsx
import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import DisenoPasajero from "../../diseños/DisenoPasajero";
import { solicitarViaje, simularPasajeroAleatorio } from "../../api";

export default function PasajeroSolicitud() {
  const nav = useNavigate();
  const pasajeroId = localStorage.getItem("pasajero_id") || "";
  const loc = useLocation() as {
    state?: { lat: number; lon: number; dest_id: string; precio: number };
  };

  const [cargando, setCargando] = useState(false);
  const [viajeId, setViajeId] = useState<string | null>(null);

  async function handleSolicitar() {
    if (!loc.state) {
      alert("Faltan datos de lat/lon/destino (vuelve a cotizar)");
      return;
    }
    if (!pasajeroId) {
      alert("No hay pasajero_id (regístrate o haz login)");
      return;
    }
    setCargando(true);
    try {
      const r = await solicitarViaje(
        pasajeroId,
        loc.state.lat,
        loc.state.lon,
        loc.state.dest_id
      );
      setViajeId(r.viaje_id);
    } finally {
      setCargando(false);
    }
  }

  async function handleSolicitarAleatorio(dest_id: string) {
    if (!pasajeroId) {
      alert("No hay pasajero_id (regístrate o haz login)");
      return;
    }
    setCargando(true);
    try {
      const r = await simularPasajeroAleatorio(pasajeroId, dest_id);
      setViajeId(r.viaje_id);
    } finally {
      setCargando(false);
    }
  }

  return (
    <div className="layout">
      <DisenoPasajero>
        <h2>Solicitar viaje</h2>
        <p>
          Pasajero: <strong>{pasajeroId}</strong>
        </p>

        {loc.state && (
          <div className="tarifa-box">
            <p>
              Origen: {loc.state.lat.toFixed(5)},{" "}
              {loc.state.lon.toFixed(5)}
            </p>
            <p>Destino ID: {loc.state.dest_id}</p>
            <p>Precio estimado: {loc.state.precio.toFixed(2)} €</p>
          </div>
        )}

        <div className="botones-columna">
          <button onClick={handleSolicitar} disabled={cargando}>
            Usar mi posición indicada
          </button>
          <button
            onClick={() => handleSolicitarAleatorio("RET")}
            disabled={cargando}
          >
            Simular pasajero aleatorio → RETIRO
          </button>
        </div>

        {viajeId && (
          <>
            <p>
              Viaje creado: <strong>{viajeId}</strong>
            </p>
            <button onClick={() => nav(`/pasajero/envivo/${viajeId}`)}>
              Ver estado en vivo
            </button>
          </>
        )}
      </DisenoPasajero>
    </div>
  );
}
