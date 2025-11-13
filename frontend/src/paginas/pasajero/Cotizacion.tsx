// frontend/src/paginas/pasajero/Cotizacion.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DisenoPasajero from "../../diseños/DisenoPasajero";
import SelectorDestino from "../../componentes/SelectorDestino";
import Mapa from "../../componentes/Mapa";
import DesgloseTarifa from "../../componentes/DesgloseTarifa";
import { cotizar } from "../../api";

export default function PasajeroCotizacion() {
  const nav = useNavigate();
  const pasajeroId = localStorage.getItem("pasajero_id") || "";
  const [lat, setLat] = useState(40.4168);
  const [lon, setLon] = useState(-3.7038);
  const [dest, setDest] = useState("");
  const [resultado, setResultado] = useState<{
    precio: number;
    eta_min: number;
  } | null>(null);

  async function handleCotizar(e: React.FormEvent) {
    e.preventDefault();
    if (!dest) {
      alert("Selecciona un destino");
      return;
    }
    const r = await cotizar(lat, lon, dest);
    setResultado({ precio: r.precio, eta_min: r.eta_min });
  }

  return (
    <div className="layout">
      <DisenoPasajero>
        <h2>Cotizar viaje</h2>
        <p style={{ fontSize: 12, opacity: 0.7 }}>
          Pasajero actual: <strong>{pasajeroId || "(no definido)"}</strong>
        </p>
        <form onSubmit={handleCotizar} className="form">
          <div className="campo-doble">
            <div className="campo">
              <label>Latitud</label>
              <input
                type="number"
                value={lat}
                onChange={(e) => setLat(parseFloat(e.target.value))}
              />
            </div>
            <div className="campo">
              <label>Longitud</label>
              <input
                type="number"
                value={lon}
                onChange={(e) => setLon(parseFloat(e.target.value))}
              />
            </div>
          </div>

          <SelectorDestino value={dest} onChange={setDest} />

          <button type="submit">Calcular tarifa</button>
        </form>

        <Mapa lat={lat} lon={lon} />

        {resultado && (
          <>
            <DesgloseTarifa
              precio={resultado.precio}
              eta_min={resultado.eta_min}
            />
            <button
              onClick={() =>
                nav("/pasajero/solicitar", {
                  state: { lat, lon, dest_id: dest, precio: resultado.precio },
                })
              }
            >
              Solicitar viaje con estos datos
            </button>
          </>
        )}
      </DisenoPasajero>
    </div>
  );
}
