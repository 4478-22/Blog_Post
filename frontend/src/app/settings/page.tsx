"use client";

import { useState, useEffect } from "react";
import { useAuthStore } from "@/store/auth-store";
import api from "@/lib/api";
import { useToast } from "@/components/Toast";

export default function SettingsPage() {
  const { user } = useAuthStore();
  const { pushToast } = useToast();
  const [bio, setBio] = useState("");
  const [avatar, setAvatar] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user?.bio) setBio(user.bio);
  }, [user]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("bio", bio);
      if (avatar) formData.append("avatar", avatar);

      await api.patch("/api/users/me/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      pushToast("Profile updated", "success");
    } catch (err) {
      pushToast("Failed to update profile", "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Bio</label>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            className="w-full rounded border px-3 py-2"
            rows={3}
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Avatar</label>
          <input type="file" onChange={(e) => setAvatar(e.target.files?.[0] || null)} />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Saving..." : "Save Changes"}
        </button>
      </form>
    </div>
  );
}
