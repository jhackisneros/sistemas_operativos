// frontend/src/paginas/Inicio.tsx
import { useNavigate } from "react-router-dom";

export default function Inicio() {
  const nav = useNavigate();

  return (
    <div className="layout">
      <div className="card">
        <h1>UNIETAXI 🚕</h1>
        <p className="subtitulo">
          Simulador de taxis con conductores y pasajeros en tiempo real.
        </p>

        <div className="botones">
          <button onClick={() => alert("Modo pasajero lo añadimos ahora")}>
            Soy pasajero
          </button>
          <button onClick={() => alert("Modo conductor lo añadimos ahora")}>
            Soy conductor
          </button>
        </div>

        <p className="nota">
          Backend: <code>http://localhost:8000</code> <br />
          Frontend: <code>http://localhost:5173</code>
        </p>
      </div>
    </div>
  );
}
