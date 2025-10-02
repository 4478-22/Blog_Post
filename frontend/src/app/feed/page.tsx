"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import PostCard, { Post } from "../../components/PostCard";
import useInfiniteScroll from "../../hooks/useInfiniteScroll";
import { useToast } from "@/components/Toast";

export default function FeedPage() {
  const { pushToast } = useToast();
  const [posts, setPosts] = useState<Post[]>([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const { lastElementRef } = useInfiniteScroll({
    hasMore,
    loading,
    onLoadMore: () => setPage((p) => p + 1),
  });

  useEffect(() => {
    let ignore = false;
    async function fetchPosts() {
      setLoading(true);
      try {
        const res = await api.get(`/api/feed/?page=${page}`);
        if (!ignore) {
          setPosts((prev) => [...prev, ...res.data.results]);
          if (!res.data.next) setHasMore(false);
        }
      } catch {
        pushToast("Failed to load feed", "error");
      } finally {
        setLoading(false);
      }
    }
    fetchPosts();
    return () => {
      ignore = true;
    };
  }, [page, pushToast]);

  return (
    <div className="max-w-2xl mx-auto mt-8 space-y-4">
      <h1 className="text-2xl font-bold mb-4">Your Feed</h1>
      {posts.map((post, i) => (
        <div
          key={post.id}
          ref={i === posts.length - 1 ? lastElementRef : null}
        >
          <PostCard post={post} />
        </div>
      ))}
      {loading && <p className="text-center">Loading...</p>}
      {!hasMore && <p className="text-center text-gray-500">No more posts</p>}
    </div>
  );
}
