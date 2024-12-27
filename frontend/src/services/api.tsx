import axios, { AxiosInstance } from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (
  email: string,
  password: string
): Promise<{ access_token: string }> => {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
};

export const createUser = async (
  userData: { name: string; email: string; password: string; role: string },
  token: string
) => {
  const response = await axios.post(`${API_URL}/users`, userData, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const getAllUsers = async () => {
  const response = await api.get("/users/all");
  return response.data;
};

export const getAllMaterials = async () => {
  const response = await api.get("/materials");
  return response.data;
};

export const createMaterial = async (materialData: any) => {
  const response = await api.post("/materials", materialData);
  return response.data;
};

export const getMaterialTracking = async (materialId: number) => {
  const response = await api.get(`/materials/${materialId}/tracking`);
  return response.data;
};

export default api;
