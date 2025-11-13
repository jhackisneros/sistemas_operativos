// frontend/src/paginas/conductor/Cuenta.tsx
import DisenoConductor from "../../diseños/DisenoConductor";

export default function ConductorCuenta() {
  const conductorId = localStorage.getItem("conductor_id") || "";
  const nombre = localStorage.getItem("conductor_nombre") || "Conductor";

  return (
    <div className="layout">
      <DisenoConductor>
        <h2>Mi cuenta</h2>
        <p>
          Nombre: <strong>{nombre}</strong>
        </p>
        <p>
          ID: <strong>{conductorId}</strong>
        </p>
        <p style={{ fontSize: 12, opacity: 0.7 }}>
          Aquí podrías mostrar documentos, estado de verificación, etc.
        </p>
      </DisenoConductor>
    </div>
  );
}
