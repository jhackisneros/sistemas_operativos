// frontend/src/paginas/conductor/Viajes.tsx
import DisenoConductor from "../../diseños/DisenoConductor";

export default function ConductorViajes() {
  const conductorId = localStorage.getItem("conductor_id") || "";

  return (
    <div className="layout">
      <DisenoConductor>
        <h2>Mis viajes</h2>
        <p>
          (Aquí podrías listar los viajes desde un endpoint como
          /conductor/viajes en el backend).
        </p>
        <p>
          ID conductor actual: <strong>{conductorId}</strong>
        </p>
      </DisenoConductor>
    </div>
  );
}
