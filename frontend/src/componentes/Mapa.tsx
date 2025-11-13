// frontend/src/componentes/Mapa.tsx
type Props = {
  lat: number;
  lon: number;
};

export default function Mapa({ lat, lon }: Props) {
  return (
    <div className="mapa-placeholder">
      <p>
        📍 Posición aproximada: <strong>{lat.toFixed(5)}</strong>,{" "}
        <strong>{lon.toFixed(5)}</strong>
      </p>
      <p style={{ fontSize: 12, opacity: 0.7 }}>
        (Aquí podrías integrar Leaflet/Mapbox más adelante)
      </p>
    </div>
  );
}
