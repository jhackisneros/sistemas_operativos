// frontend/src/componentes/TarjetaEstadisticas.tsx
type Props = {
  titulo: string;
  items: { label: string; valor: string | number }[];
};

export default function TarjetaEstadisticas({ titulo, items }: Props) {
  return (
    <div className="tarjeta-estadisticas">
      <h3>{titulo}</h3>
      <ul>
        {items.map((it) => (
          <li key={it.label}>
            <span>{it.label}</span>
            <strong>{it.valor}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}
