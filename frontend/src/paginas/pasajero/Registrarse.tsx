// frontend/src/paginas/pasajero/Registrarse.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DisenoPasajero from "../../diseños/DisenoPasajero";

export default function PasajeroRegistrarse() {
  const [nombre, setNombre] = useState("");
  const nav = useNavigate();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const id = "P-" + Math.random().toString(16).slice(2, 8);
    localStorage.setItem("pasajero_id", id);
    localStorage.setItem("pasajero_nombre", nombre || "Pasajero");
    alert(`Tu ID pasajero es: ${id} (guardado en el navegador)`);
    nav("/pasajero/cotizar");
  }

  return (
    <div className="layout">
      <DisenoPasajero>
        <h2>Registro pasajero</h2>
        <form onSubmit={handleSubmit} className="form">
          <div className="campo">
            <label>Nombre</label>
            <input
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              placeholder="Tu nombre"
            />
          </div>
          <button type="submit">Crear pasajero</button>
        </form>
      </DisenoPasajero>
    </div>
  );
}
