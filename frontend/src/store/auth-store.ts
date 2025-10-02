// src/store/auth-store.ts
import { create } from "zustand";
import { setTokens, getTokens, clearTokens, Tokens } from "@/lib/auth";
import api from "@/lib/api";

type User = {
  id: number;
  username: string;
  email: string;
  bio?: string;       // optional profile bio
  avatar?: string;
  followers_count?: number;
  following_count?: number;
};

type AuthState = {
  user: User | null;
  tokens: Tokens | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  hydrate: () => void;
  setTokens: (tokens: Tokens) => void;
};

function setAuthCookie(value: boolean) {
  if (value) {
    // Persistent cookie, valid for 7 days (adjust if needed)
    document.cookie = `auth=true; path=/; max-age=${7 * 24 * 60 * 60}`;
  } else {
    // Expire cookie immediately
    document.cookie =
      "auth=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  tokens: null,

  setTokens: (tokens) => {
    set({ tokens });
    setTokens(tokens);
  },

  login: async (username, password) => {
    const res = await api.post("/api/auth/jwt/create/", { username, password });
    const tokens = {
      access: res.data.access,
      refresh: res.data.refresh,
    };
    setTokens(tokens);
    set({ tokens });

    // Fetch current user
    const me = await api.get("/api/users/me/", {
      headers: { Authorization: `Bearer ${tokens.access}` },
    });
    set({ user: me.data });

    // ✅ Set auth cookie for middleware
    setAuthCookie(true);
  },

  logout: () => {
    clearTokens();
    set({ user: null, tokens: null });

    // ✅ Clear auth cookie for middleware
    setAuthCookie(false);
  },

  hydrate: () => {
    const stored = getTokens();
    if (stored) {
      set({ tokens: stored });
      api
        .get("/api/users/me/")
        .then((res) => {
          set({ user: res.data });
          setAuthCookie(true);
        })
        .catch(() => {
          clearTokens();
          setAuthCookie(false);
        });
    }
  },
}));
