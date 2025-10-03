"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";
import api from "@/lib/api";
import PostCard from "@/components/PostCard";
import { useToast } from "@/components/Toast";

function SearchResults() {
  const q = useSearchParams().get("q") || "";
  const { pushToast } = useToast();

  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!q) return;
    setLoading(true);
    api
      .get(`/api/posts/search/?q=${encodeURIComponent(q)}`)
      .then((res) => setResults(res.data))
      .catch(() => pushToast("Search failed", "error"))
      .finally(() => setLoading(false));
  }, [q, pushToast]);

  if (!q) return <p className="text-gray-500">Enter a search term...</p>;

  return (
    <div className="max-w-2xl mx-auto mt-10 space-y-4">
      <h1 className="text-xl font-bold">Search Results for "{q}"</h1>
      {loading && <p>Loading...</p>}
      {!loading && results.length === 0 && (
        <p className="text-gray-500">No posts found.</p>
      )}
      <div className="space-y-4">
        {results.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<p className="text-gray-500">Loading search...</p>}>
      <SearchResults />
    </Suspense>
  );
}
