"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { useAuthStore } from "@/store/auth-store";
import { useToast } from "@/components/Toast";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const { pushToast } = useToast();

  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.username || !form.password) {
      pushToast("All fields are required", "error");
      return;
    }

    setLoading(true);
    try {
      await login(form.username, form.password); // ✅ Call store only
      pushToast("Login successful", "success");
      router.push("/feed");
    } catch (err: any) {
      pushToast(err.response?.data?.detail || "Login failed", "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16">
      <h1 className="text-2xl font-bold mb-6">Login</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Username or Email"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <Input
          type="password"
          label="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <Button type="submit" loading={loading}>
          Login
        </Button>
      </form>
    </div>
  );
}
