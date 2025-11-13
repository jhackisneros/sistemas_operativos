// frontend/src/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Ejemplo de llamada: listar destinos
export const getDestinos = async () => (await api.get("/comunes/destinos")).data;

export default api;
