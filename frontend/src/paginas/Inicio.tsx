// frontend/src/paginas/Inicio.tsx
import { useNavigate } from "react-router-dom";
import DisenoPasajero from "../diseños/DisenoPasajero";
import DisenoConductor from "../diseños/DisenoConductor";

export default function Inicio() {
  const nav = useNavigate();

  return (
    <div className="layout layout-dos-columnas">
      <DisenoPasajero>
        <h1>UNIETAXI 🚕</h1>
        <p className="subtitulo">
          Simulador de pasajeros: calcula precio, solicita un viaje y sigue tu
          taxi en tiempo simulado.
        </p>
        <div className="botones">
          <button onClick={() => nav("/pasajero/registro")}>Registrarme</button>
          <button onClick={() => nav("/pasajero/login")}>Ya tengo ID</button>
        </div>
      </DisenoPasajero>

      <DisenoConductor>
        <h1>Zona conductor 🧑‍✈️</h1>
        <p className="subtitulo">
          Date de alta, valida tus datos y ponte ONLINE para recibir viajes.
        </p>
        <div className="botones">
          <button onClick={() => nav("/conductor/registro")}>Registrarme</button>
          <button onClick={() => nav("/conductor/login")}>Ya soy conductor</button>
        </div>
      </DisenoConductor>
    </div>
  );
}
