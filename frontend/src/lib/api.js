import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

const api = axios.create({ baseURL: API });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("fz_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      localStorage.removeItem("fz_token");
    }
    return Promise.reject(err);
  }
);

export const setToken = (t) => localStorage.setItem("fz_token", t);
export const clearToken = () => localStorage.removeItem("fz_token");
export const getToken = () => localStorage.getItem("fz_token");

export const rupee = (n) =>
  "₹" + Number(n || 0).toLocaleString("en-IN");

export const downloadArtifact = async (artifactId, filename) => {
  const res = await api.get(`/downloads/${artifactId}`, { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const a = document.createElement("a");
  a.href = url;
  a.download = filename || "download";
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
};

export default api;
