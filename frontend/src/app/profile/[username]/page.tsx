"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import Avatar from "@/components/Avatar";
import PostCard from "@/components/PostCard";
import { useToast } from "@/components/Toast";

type UserProfile = {
  id: number;
  username: string;
  email: string;
  bio?: string;
  avatar?: string;
  followers_count?: number;
  following_count?: number;
};

export default function ProfilePage() {
  const { username } = useParams<{ username: string }>();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [posts, setPosts] = useState<any[]>([]);
  const { pushToast } = useToast();

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await api.get(`/api/users/?username=${username}`);
        setProfile(res.data[0]); // assuming backend supports ?username=

        const postsRes = await api.get(`/api/posts/?author=${username}`);
        setPosts(postsRes.data);
      } catch (err) {
        pushToast("Failed to load profile", "error");
      }
    }
    fetchData();
  }, [username, pushToast]);

  if (!profile) return <p className="mt-10 text-center">Loading...</p>;

  return (
    <div className="max-w-2xl mx-auto mt-10 space-y-6">
      {/* User info */}
      <div className="flex items-center space-x-4">
        <Avatar src={profile.avatar} alt={profile.username} size={80} />
        <div>
          <h1 className="text-2xl font-bold">{profile.username}</h1>
          <p className="text-gray-600">{profile.bio || "No bio yet"}</p>
          <div className="flex space-x-4 text-sm text-gray-500 mt-2">
            <span>{profile.followers_count ?? 0} Followers</span>
            <span>{profile.following_count ?? 0} Following</span>
          </div>
        </div>
      </div>

      {/* Follow/Unfollow placeholder */}
      <button className="px-4 py-2 bg-blue-500 text-white rounded">
        Follow / Unfollow
      </button>

      {/* Posts */}
      <div className="space-y-4">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}
