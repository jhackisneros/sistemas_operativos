// frontend/src/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// ===== COMUNES =====
export type Destino = {
  id: string;
  nombre: string;
  descripcion: string;
  lat: number;
  lon: number;
};

export const getDestinos = async (): Promise<Destino[]> =>
  (await api.get("/comunes/destinos")).data;

export const cotizar = async (
  lat: number,
  lon: number,
  dest_id: string
): Promise<{ precio: number; eta_min: number; momento_sim: string }> =>
  (await api.post(`/pasajero/cotizar?lat=${lat}&lon=${lon}&dest_id=${dest_id}`))
    .data;

// ===== PASAJERO =====
export const solicitarViaje = async (
  pasajero_id: string,
  lat: number,
  lon: number,
  dest_id: string
): Promise<{ viaje_id: string; precio: number }> =>
  (
    await api.post(
      `/pasajero/solicitar?pasajero_id=${pasajero_id}&lat=${lat}&lon=${lon}&dest_id=${dest_id}`
    )
  ).data;

export const simularPasajeroAleatorio = async (
  pasajero_id: string,
  dest_id: string
): Promise<{ viaje_id: string; precio: number }> =>
  (await api.post(`/pasajero/simular_aleatorio?pasajero_id=${pasajero_id}&dest_id=${dest_id}`))
    .data;

// ===== CONDUCTOR =====
export const registrarConductor = async (data: {
  conductor_id: string;
  nombre: string;
  licencia_ok: boolean;
  antecedentes_ok: boolean;
  placa: string;
  marca: string;
  modelo: string;
  lat: number;
  lon: number;
}) => (await api.post("/conductor/registrar", null, { params: data })).data;

export const conductorOnline = async (
  conductor_id: string,
  lat: number,
  lon: number
) =>
  (
    await api.post(
      `/conductor/online?conductor_id=${conductor_id}&lat=${lat}&lon=${lon}`
    )
  ).data;

export const conductorOffline = async (conductor_id: string) =>
  (await api.post(`/conductor/offline?conductor_id=${conductor_id}`)).data;

export default api;
