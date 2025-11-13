// frontend/src/paginas/conductor/Tablero.tsx
import { useState } from "react";
import DisenoConductor from "../../diseños/DisenoConductor";
import { conductorOnline, conductorOffline } from "../../api";
import TarjetaEstadisticas from "../../componentes/TarjetaEstadisticas";

export default function ConductorTablero() {
  const conductorId = localStorage.getItem("conductor_id") || "";
  const nombre = localStorage.getItem("conductor_nombre") || "Conductor";
  const [online, setOnline] = useState(false);
  const [lat, setLat] = useState(40.4168);
  const [lon, setLon] = useState(-3.7038);

  async function handleOnline() {
    if (!conductorId) {
      alert("No hay conductor_id, regístrate primero.");
      return;
    }
    const r = await conductorOnline(conductorId, lat, lon);
    console.log(r);
    setOnline(true);
  }

  async function handleOffline() {
    if (!conductorId) return;
    const r = await conductorOffline(conductorId);
    console.log(r);
    setOnline(false);
  }

  return (
    <div className="layout">
      <DisenoConductor>
        <h2>Tablero conductor</h2>
        <p>
          Bienvenido, <strong>{nombre}</strong> ({conductorId || "sin ID"})
        </p>

        <div className="campo-doble">
          <div className="campo">
            <label>Latitud actual</label>
            <input
              type="number"
              value={lat}
              onChange={(e) => setLat(parseFloat(e.target.value))}
            />
          </div>
          <div className="campo">
            <label>Longitud actual</label>
            <input
              type="number"
              value={lon}
              onChange={(e) => setLon(parseFloat(e.target.value))}
            />
          </div>
        </div>

        <div className="botones">
          {!online ? (
            <button onClick={handleOnline}>Ponerme ONLINE</button>
          ) : (
            <button onClick={handleOffline}>Ponerme OFFLINE</button>
          )}
        </div>

        <TarjetaEstadisticas
          titulo="Resumen (simulado)"
          items={[
            { label: "Estado", valor: online ? "ONLINE" : "OFFLINE" },
            { label: "Posición lat", valor: lat.toFixed(4) },
            { label: "Posición lon", valor: lon.toFixed(4) },
          ]}
        />
      </DisenoConductor>
    </div>
  );
}
