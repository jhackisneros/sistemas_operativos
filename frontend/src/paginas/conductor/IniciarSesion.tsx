// frontend/src/paginas/conductor/IniciarSesion.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DisenoConductor from "../../diseños/DisenoConductor";

export default function ConductorIniciarSesion() {
  const [id, setId] = useState(localStorage.getItem("conductor_id") || "");
  const nav = useNavigate();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!id) {
      alert("Introduce tu ID de conductor");
      return;
    }
    localStorage.setItem("conductor_id", id);
    nav("/conductor/tablero");
  }

  return (
    <div className="layout">
      <DisenoConductor>
        <h2>Entrar como conductor</h2>
        <form onSubmit={handleSubmit} className="form">
          <div className="campo">
            <label>ID conductor</label>
            <input
              value={id}
              onChange={(e) => setId(e.target.value)}
              placeholder="C-xxxxxx"
            />
          </div>
          <button type="submit">Continuar</button>
        </form>
      </DisenoConductor>
    </div>
  );
}
