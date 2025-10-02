"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import PostCard from "@/components/PostCard";
import CommentList from "../../../components/CommentList";
import Button from "@/components/ui/Button";
import { useToast } from "@/components/Toast";

export default function PostDetailPage() {
  const { id } = useParams();
  const { pushToast } = useToast();

  const [post, setPost] = useState<any>(null);
  const [comments, setComments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [newComment, setNewComment] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function fetchData() {
    try {
      const [postRes, commentsRes] = await Promise.all([
        api.get(`/api/posts/${id}/`),
        api.get(`/api/comments/?post=${id}`),
      ]);
      setPost(postRes.data);
      setComments(commentsRes.data);
    } catch {
      pushToast("Failed to load post", "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, [id]);

  async function handleComment(e: React.FormEvent) {
    e.preventDefault();
    if (!newComment.trim()) return;
    setSubmitting(true);
    try {
      await api.post("/api/comments/", { post: id, content: newComment });
      setNewComment("");
      pushToast("Comment added", "success");
      fetchData();
    } catch {
      pushToast("Failed to add comment", "error");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <p className="text-center mt-10">Loading...</p>;

  if (!post) return <p className="text-center mt-10">Post not found.</p>;

  return (
    <div className="max-w-2xl mx-auto mt-10 space-y-6">
      {/* Post */}
      <PostCard post={post} />

      {/* Comments */}
      <section>
        <h2 className="text-lg font-bold mb-4">Comments</h2>
        <CommentList comments={comments} />

        {/* Comment form */}
        <form onSubmit={handleComment} className="mt-4 space-y-2">
          <textarea
            className="w-full border rounded-md p-2"
            rows={3}
            placeholder="Write a comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
          />
          <Button type="submit" loading={submitting}>
            Add Comment
          </Button>
        </form>
      </section>
    </div>
  );
}
