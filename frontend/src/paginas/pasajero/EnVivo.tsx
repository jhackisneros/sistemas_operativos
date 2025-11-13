// frontend/src/paginas/pasajero/EnVivo.tsx
import { useParams } from "react-router-dom";
import DisenoPasajero from "../../diseños/DisenoPasajero";
import EstadoEnVivo from "../../componentes/EstadoEnVivo";

export default function PasajeroEnVivo() {
  const { viajeId } = useParams<{ viajeId: string }>();

  if (!viajeId) {
    return <p>Falta viajeId en la URL.</p>;
  }

  return (
    <div className="layout">
      <DisenoPasajero>
        <h2>Seguimiento del viaje</h2>
        <p>
          ID del viaje: <strong>{viajeId}</strong>
        </p>
        <EstadoEnVivo viajeId={viajeId} />
      </DisenoPasajero>
    </div>
  );
}
