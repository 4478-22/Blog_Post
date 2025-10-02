"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/auth-store";

export default function ClientHydrate({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    useAuthStore.getState().hydrate();
  }, []);

  return <>{children}</>;
}
