"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { useToast } from "@/components/Toast";

export default function ComposePage() {
  const router = useRouter();
  const { pushToast } = useToast();

  const [content, setContent] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!content.trim() && !file) {
      pushToast("Post must have text or image", "error");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("content", content);
      if (file) {
        formData.append("image", file);
      }

      await api.post("/api/posts/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      pushToast("Post created successfully", "success");
      router.push("/feed");
    } catch (err: any) {
      pushToast(err.response?.data?.detail || "Failed to create post", "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-lg mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-6">Compose a Post</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          className="w-full border rounded-md p-2"
          rows={4}
          placeholder="What's on your mind?"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <Input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <Button type="submit" loading={loading} className="w-full">
          Post
        </Button>
      </form>
    </div>
  );
}
