type Comment = {
  id: number;
  author: { username: string };
  content: string;
  created_at: string;
};

export default function CommentList({ comments }: { comments: Comment[] }) {
  if (!comments || comments.length === 0) {
    return <p className="text-sm text-gray-500">No comments yet.</p>;
  }

  return (
    <ul className="space-y-4">
      {comments.map((c) => (
        <li key={c.id} className="border-b pb-2">
          <p className="text-sm font-semibold">{c.author.username}</p>
          <p className="text-sm">{c.content}</p>
          <p className="text-xs text-gray-400">{new Date(c.created_at).toLocaleString()}</p>
        </li>
      ))}
    </ul>
  );
}
