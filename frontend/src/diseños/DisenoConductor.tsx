// frontend/src/diseños/DisenoConductor.tsx
import { ReactNode } from "react";

export default function DisenoConductor({ children }: { children: ReactNode }) {
  return (
    <div className="card card-conductor">
      {children}
    </div>
  );
}
