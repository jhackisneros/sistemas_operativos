// frontend/src/paginas/conductor/Registrarse.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DisenoConductor from "../../diseños/DisenoConductor";
import { registrarConductor } from "../../api";

export default function ConductorRegistrarse() {
  const [nombre, setNombre] = useState("");
  const [placa, setPlaca] = useState("");
  const [marca, setMarca] = useState("Toyota");
  const [modelo, setModelo] = useState("Corolla");
  const [lat, setLat] = useState(40.4168);
  const [lon, setLon] = useState(-3.7038);
  const [antecedentes, setAntecedentes] = useState(false);
  const nav = useNavigate();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const conductor_id = "C-" + Math.random().toString(16).slice(2, 8);
    const resp = await registrarConductor({
      conductor_id,
      nombre,
      licencia_ok: true,
      antecedentes_ok: !antecedentes,
      placa,
      marca,
      modelo,
      lat,
      lon,
    });

    if (resp.estado === "RECHAZADO") {
      alert("Conductor rechazado: antecedentes penales.");
      return;
    }

    localStorage.setItem("conductor_id", conductor_id);
    localStorage.setItem("conductor_nombre", nombre || "Conductor");

    alert(`Conductor registrado, ID: ${conductor_id}`);
    nav("/conductor/tablero");
  }

  return (
    <div className="layout">
      <DisenoConductor>
        <h2>Registro conductor</h2>
        <form onSubmit={handleSubmit} className="form">
          <div className="campo">
            <label>Nombre</label>
            <input
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
          </div>
          <div className="campo">
            <label>Placa</label>
            <input
              value={placa}
              onChange={(e) => setPlaca(e.target.value)}
              required
            />
          </div>
          <div className="campo-doble">
            <div className="campo">
              <label>Marca</label>
              <input value={marca} onChange={(e) => setMarca(e.target.value)} />
            </div>
            <div className="campo">
              <label>Modelo</label>
              <input
                value={modelo}
                onChange={(e) => setModelo(e.target.value)}
              />
            </div>
          </div>
          <div className="campo-doble">
            <div className="campo">
              <label>Latitud inicial</label>
              <input
                type="number"
                value={lat}
                onChange={(e) => setLat(parseFloat(e.target.value))}
              />
            </div>
            <div className="campo">
              <label>Longitud inicial</label>
              <input
                type="number"
                value={lon}
                onChange={(e) => setLon(parseFloat(e.target.value))}
              />
            </div>
          </div>
          <div className="campo-check">
            <label>
              <input
                type="checkbox"
                checked={antecedentes}
                onChange={(e) => setAntecedentes(e.target.checked)}
              />{" "}
              Tengo antecedentes penales (para probar rechazo)
            </label>
          </div>
          <button type="submit">Registrar conductor</button>
        </form>
      </DisenoConductor>
    </div>
  );
}
