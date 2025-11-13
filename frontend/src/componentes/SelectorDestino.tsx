// frontend/src/componentes/SelectorDestino.tsx
import { useEffect, useState } from "react";
import { Destino, getDestinos } from "../api";

type Props = {
  value: string;
  onChange: (id: string) => void;
};

export default function SelectorDestino({ value, onChange }: Props) {
  const [destinos, setDestinos] = useState<Destino[]>([]);
  const [cargando, setCargando] = useState(false);

  useEffect(() => {
    setCargando(true);
    getDestinos()
      .then(setDestinos)
      .finally(() => setCargando(false));
  }, []);

  return (
    <div className="campo">
      <label>Destino</label>
      {cargando ? (
        <p>Cargando destinos...</p>
      ) : (
        <select value={value} onChange={(e) => onChange(e.target.value)}>
          <option value="">Selecciona un destino</option>
          {destinos.map((d) => (
            <option key={d.id} value={d.id}>
              {d.nombre} ({d.id})
            </option>
          ))}
        </select>
      )}
    </div>
  );
}
