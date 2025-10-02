"use client";

import { useState } from "react";
import api from "@/lib/api";
import { useToast } from "./Toast";

export type Post = {
  id: number;
  author: { id: number; username: string };
  content: string;
  image?: string;
  likes_count: number;
  comments_count: number;
  liked: boolean;
};

export default function PostCard({ post }: { post: Post }) {
  const { pushToast } = useToast();
  const [liked, setLiked] = useState(post.liked);
  const [likes, setLikes] = useState(post.likes_count);

  async function toggleLike() {
    try {
      setLiked(!liked);
      setLikes((l) => (liked ? l - 1 : l + 1));

      if (!liked) {
        await api.post(`/api/posts/${post.id}/like/`);
      } else {
        await api.post(`/api/posts/${post.id}/unlike/`);
      }
    } catch {
      // revert optimistic update
      setLiked(liked);
      setLikes(post.likes_count);
      pushToast("Failed to update like", "error");
    }
  }

  return (
    <div className="border rounded-lg p-4 shadow-sm bg-white dark:bg-gray-900">
      <div className="flex items-center mb-2">
        <span className="font-semibold">@{post.author.username}</span>
      </div>
      <p className="mb-2">{post.content}</p>
      {post.image && (
        <img
          src={post.image}
          alt="Post image"
          className="w-full rounded-md mb-2"
        />
      )}
      <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
        <button
          onClick={toggleLike}
          className="hover:underline"
        >
          {liked ? "❤️ Unlike" : "🤍 Like"} ({likes})
        </button>
        <span>💬 {post.comments_count} comments</span>
      </div>
    </div>
  );
}
