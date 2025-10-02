// src/lib/auth.ts
export type Tokens = {
  access: string;
  refresh: string;
};

const STORAGE_KEY = "auth_tokens";

export const getTokens = (): Tokens | null => {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : null;
};

export const setTokens = (tokens: Tokens) => {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tokens));
};

export const clearTokens = () => {
  if (typeof window === "undefined") return;
  localStorage.removeItem(STORAGE_KEY);
};
