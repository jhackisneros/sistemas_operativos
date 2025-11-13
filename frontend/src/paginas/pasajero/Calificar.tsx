// frontend/src/paginas/pasajero/Calificar.tsx
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import DisenoPasajero from "../../diseños/DisenoPasajero";
import api from "../../api";

export default function PasajeroCalificar() {
  const { viajeId } = useParams<{ viajeId: string }>();
  const nav = useNavigate();
  const [puntuacion, setPuntuacion] = useState(5);
  const [comentario, setComentario] = useState("");

  if (!viajeId) {
    return (
      <div className="layout">
        <DisenoPasajero>
          <h2>Calificar viaje</h2>
          <p>Falta el ID del viaje en la URL.</p>
        </DisenoPasajero>
      </div>
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      // Aquí asumimos que en el backend tendrás un endpoint:
      // POST /pasajero/calificar  con { viaje_id, puntuacion, comentario }
      await api.post("/pasajero/calificar", {
        viaje_id: viajeId,
        puntuacion,
        comentario,
      });

      alert("¡Gracias por tu valoración! ⭐");
      nav("/"); // o /pasajero/cotizar o donde quieras mandarle
    } catch (err) {
      console.error(err);
      alert("No se pudo enviar la calificación (revisa el backend /pasajero/calificar).");
    }
  }

  return (
    <div className="layout">
      <DisenoPasajero>
        <h2>Calificar viaje</h2>
        <p>
          Estás calificando el viaje: <strong>{viajeId}</strong>
        </p>

        <form onSubmit={handleSubmit} className="form">
          <div className="campo">
            <label>Puntuación (1–5)</label>
            <input
              type="number"
              min={1}
              max={5}
              value={puntuacion}
              onChange={(e) => setPuntuacion(parseInt(e.target.value) || 1)}
            />
          </div>

          <div className="campo">
            <label>Comentario opcional</label>
            <textarea
              value={comentario}
              onChange={(e) => setComentario(e.target.value)}
              placeholder="¿Qué tal fue el servicio?"
              rows={4}
            />
          </div>

          <button type="submit">Enviar calificación</button>
        </form>
      </DisenoPasajero>
    </div>
  );
}
