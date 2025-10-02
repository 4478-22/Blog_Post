// src/lib/api.ts
import axios from "axios";
import { getTokens, setTokens, clearTokens } from "./auth";
import { useAuthStore } from "../store/auth-store";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  withCredentials: false,
});

let isRefreshing = false;
let refreshQueue: (() => void)[] = [];

// Attach Authorization header
api.interceptors.request.use((config) => {
  const tokens = getTokens();
  if (tokens?.access && config.headers) {
    config.headers.Authorization = `Bearer ${tokens.access}`;
  }
  return config;
});

// Handle 401 → try refresh
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    if (err.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        return new Promise((resolve) =>
          refreshQueue.push(() => resolve(api(original)))
        );
      }
      original._retry = true;
      isRefreshing = true;

      try {
        const { refresh } = getTokens() || {};
        if (!refresh) throw new Error("No refresh token");
        const resp = await axios.post(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/auth/jwt/refresh/`,
          { refresh }
        );
        const newTokens = {
          access: resp.data.access,
          refresh,
        };
        setTokens(newTokens);
        useAuthStore.getState().setTokens(newTokens);
        refreshQueue.forEach((cb) => cb());
        refreshQueue = [];
        return api(original);
      } catch (e) {
        clearTokens();
        useAuthStore.getState().logout();
        return Promise.reject(e);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(err);
  }
);

export default api;
