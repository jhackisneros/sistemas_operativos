// frontend/src/diseños/DisenoPasajero.tsx
import { ReactNode } from "react";

export default function DisenoPasajero({ children }: { children: ReactNode }) {
  return (
    <div className="card card-pasajero">
      {children}
    </div>
  );
}
