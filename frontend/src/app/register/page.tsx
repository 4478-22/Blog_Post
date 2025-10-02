"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import api from "@/lib/api";
import { useAuthStore } from "@/store/auth-store";
import { useToast } from "@/components/Toast";

export default function RegisterPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const { pushToast } = useToast();

  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.username || !form.email || !form.password) {
      pushToast("All fields are required", "error");
      return;
    }

    setLoading(true);
    try {
      // Register new user
      await api.post("/api/auth/register/", form);

      // ✅ Immediately login with same credentials
      await login(form.username, form.password);

      pushToast("Registration successful", "success");
      router.push("/feed");
    } catch (err: any) {
      pushToast(err.response?.data?.detail || "Registration failed", "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16">
      <h1 className="text-2xl font-bold mb-6">Register</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Username"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <Input
          label="Email"
          type="email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <Input
          type="password"
          label="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <Button type="submit" loading={loading}>
          Register
        </Button>
      </form>
    </div>
  );
}
