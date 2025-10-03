"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import PostCard from "@/components/PostCard";
import { useToast } from "@/components/Toast";
import { useAuthStore } from "@/store/auth-store";

export default function FeedPage() {
  const { pushToast } = useToast();
  const { user } = useAuthStore();   //check if logged in
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) return; //don’t fetch if not logged in

    setLoading(true);
    api.get("/api/feed/")
      .then((res) => setPosts(res.data.results))
      .catch((err) => {
        if (err.response?.status === 401) {
          pushToast("Please log in to see your feed", "info");
        } else {
          pushToast("Failed to load feed", "error");
        }
      })
      .finally(() => setLoading(false));
  }, [user]);

  if (!user) {
    return (
      <div className="max-w-2xl mx-auto mt-10 text-gray-500 text-center">
        Please log in to see your feed.
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 space-y-4">
      <h1 className="text-xl font-bold">Your Feed</h1>
      {loading && <p>Loading...</p>}
      {!loading && posts.length === 0 && (
        <p className="text-gray-500">No posts in your feed yet.</p>
      )}
      <div className="space-y-4">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}
