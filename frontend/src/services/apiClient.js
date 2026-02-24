import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const instance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000
});

export const apiClient = {
  setToken(token) {
    if (token) {
      instance.defaults.headers.common.Authorization = `Bearer ${token}`;
    } else {
      delete instance.defaults.headers.common.Authorization;
    }
  },
  get: (...args) => instance.get(...args),
  post: (...args) => instance.post(...args)
};

