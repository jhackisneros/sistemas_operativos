// frontend/src/componentes/DesgloseTarifa.tsx
type Props = {
  precio: number;
  eta_min: number;
};

export default function DesgloseTarifa({ precio, eta_min }: Props) {
  return (
    <div className="tarifa-box">
      <h3>Resumen del viaje</h3>
      <p>
        <strong>Precio estimado:</strong> {precio.toFixed(2)} €
      </p>
      <p>
        <strong>Tiempo estimado:</strong> {eta_min.toFixed(1)} min
      </p>
      <p style={{ fontSize: 12, opacity: 0.7 }}>
        La simulación aplica tarifa base + km + suplementos (T4, nocturno,
        etc.).
      </p>
    </div>
  );
}
