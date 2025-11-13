// frontend/src/componentes/SelectorDestino.tsx
import { useEffect, useState } from "react";
import { Destino, getDestinos } from "../api";

type Props = {
  value: string;
  onChange: (id: string) => void;
};

// Fallback por si el backend no responde o devuelve lista vacía
const DESTINOS_FIJOS: Destino[] = [
  {
    id: "RET",
    nombre: "Parque del Retiro",
    descripcion: "Parque emblemático de Madrid, zona centro-este.",
    lat: 40.41526,
    lon: -3.684419,
  },
  {
    id: "BER",
    nombre: "Estadio Santiago Bernabéu",
    descripcion: "Estadio del Real Madrid, Paseo de la Castellana.",
    lat: 40.45306,
    lon: -3.688344,
  },
  {
    id: "CDC",
    nombre: "Casa de Campo",
    descripcion: "Gran parque al oeste de Madrid.",
    lat: 40.41799,
    lon: -3.75318,
  },
  {
    id: "MAT",
    nombre: "Matadero Madrid",
    descripcion: "Centro cultural en la zona de Legazpi.",
    lat: 40.39164,
    lon: -3.69825,
  },
  {
    id: "T4",
    nombre: "Aeropuerto T4 Barajas",
    descripcion: "Terminal T4 del aeropuerto de Madrid.",
    lat: 40.49184,
    lon: -3.59335,
  },
];

export default function SelectorDestino({ value, onChange }: Props) {
  const [destinos, setDestinos] = useState<Destino[]>([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelado = false;

    async function cargar() {
      setCargando(true);
      setError(null);
      try {
        const desdeApi = await getDestinos();
        if (!cancelado) {
          if (desdeApi && desdeApi.length > 0) {
            setDestinos(desdeApi);
          } else {
            // si la API devuelve vacío, usamos los fijos
            setDestinos(DESTINOS_FIJOS);
          }
        }
      } catch (e) {
        console.error("Error cargando destinos:", e);
        if (!cancelado) {
          setError("No se pudieron cargar los destinos desde el servidor. Usando lista fija.");
          setDestinos(DESTINOS_FIJOS);
        }
      } finally {
        if (!cancelado) {
          setCargando(false);
        }
      }
    }

    cargar();

    return () => {
      cancelado = true;
    };
  }, []);

  return (
    <div className="campo">
      <label>Destino</label>

      {cargando && <p>Cargando destinos...</p>}

      {error && (
        <p style={{ color: "#f97373", fontSize: 12 }}>
          {error}
        </p>
      )}

      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">Selecciona un destino</option>
        {destinos.map((d) => (
          <option key={d.id} value={d.id}>
            {d.nombre} ({d.id})
          </option>
        ))}
      </select>
    </div>
  );
}
