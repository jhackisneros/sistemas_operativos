// frontend/src/paginas/pasajero/IniciarSesion.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DisenoPasajero from "../../diseños/DisenoPasajero";

export default function PasajeroIniciarSesion() {
  const [id, setId] = useState(localStorage.getItem("pasajero_id") || "");
  const nav = useNavigate();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!id) {
      alert("Introduce tu ID de pasajero");
      return;
    }
    localStorage.setItem("pasajero_id", id);
    nav("/pasajero/cotizar");
  }

  return (
    <div className="layout">
      <DisenoPasajero>
        <h2>Entrar como pasajero</h2>
        <form onSubmit={handleSubmit} className="form">
          <div className="campo">
            <label>ID pasajero</label>
            <input
              value={id}
              onChange={(e) => setId(e.target.value)}
              placeholder="P-xxxxxx"
            />
          </div>
          <button type="submit">Continuar</button>
        </form>
      </DisenoPasajero>
    </div>
  );
}
