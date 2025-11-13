// frontend/src/rutas.tsx
import { Routes, Route } from "react-router-dom";
import Inicio from "./paginas/Inicio";

// Pasajero
import PasajeroCotizacion from "./paginas/pasajero/Cotizacion";
import PasajeroSolicitud from "./paginas/pasajero/Solicitud";
import PasajeroEnVivo from "./paginas/pasajero/EnVivo";
import PasajeroRegistrarse from "./paginas/pasajero/Registrarse";
import PasajeroIniciarSesion from "./paginas/pasajero/IniciarSesion";

// Conductor
import ConductorRegistrarse from "./paginas/conductor/Registrarse";
import ConductorIniciarSesion from "./paginas/conductor/IniciarSesion";
import ConductorTablero from "./paginas/conductor/Tablero";
import ConductorViajes from "./paginas/conductor/Viajes";
import ConductorCuenta from "./paginas/conductor/Cuenta";

export default function Rutas() {
  return (
    <Routes>
      <Route path="/" element={<Inicio />} />

      {/* PASAJERO */}
      <Route path="/pasajero/registro" element={<PasajeroRegistrarse />} />
      <Route path="/pasajero/login" element={<PasajeroIniciarSesion />} />
      <Route path="/pasajero/cotizar" element={<PasajeroCotizacion />} />
      <Route path="/pasajero/solicitar" element={<PasajeroSolicitud />} />
      <Route path="/pasajero/envivo/:viajeId" element={<PasajeroEnVivo />} />

      {/* CONDUCTOR */}
      <Route path="/conductor/registro" element={<ConductorRegistrarse />} />
      <Route path="/conductor/login" element={<ConductorIniciarSesion />} />
      <Route path="/conductor/tablero" element={<ConductorTablero />} />
      <Route path="/conductor/viajes" element={<ConductorViajes />} />
      <Route path="/conductor/cuenta" element={<ConductorCuenta />} />
    </Routes>
  );
}
