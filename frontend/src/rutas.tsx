// frontend/src/rutas.tsx
import { Routes, Route } from "react-router-dom";
import Inicio from "./paginas/Inicio";

export default function Rutas() {
  return (
    <Routes>
      <Route path="/" element={<Inicio />} />
      {/* Más rutas después: pasajero, conductor, etc. */}
    </Routes>
  );
}
