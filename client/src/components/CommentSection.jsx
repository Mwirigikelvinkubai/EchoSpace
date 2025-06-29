import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

export default function CommentSection({ postId }) {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [content, setContent] = useState("");

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/api/posts/${postId}/comments`)
      .then(res => res.json())
      .then(data => setComments(data));
  }, [postId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;

    const res = await fetch("http://127.0.0.1:5000/api/comments", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // ✅ use cookies
      body: JSON.stringify({ post_id: postId, content }),
    });

    if (res.ok) {
      const newComment = await res.json();
      setComments(prev => [...prev, newComment]);
      setContent("");
    }
  };

  return (
    <div className="mt-4 border-t pt-4">
      <h3 className="font-semibold mb-2">Comments</h3>

      {comments.length === 0 && <p className="text-gray-500">No comments yet.</p>}

      <ul className="space-y-2 mb-4">
        {comments.map(comment => (
          <li key={comment.id} className="border p-2 rounded bg-gray-50">
            <p className="text-sm text-gray-700">
              <strong>{comment.user}</strong>: {comment.content}
            </p>
            <p className="text-xs text-gray-400">
              {new Date(comment.timestamp).toLocaleString()}
            </p>
          </li>
        ))}
      </ul>

      {user && (
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
          <textarea
            rows="2"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="p-2 border rounded"
            placeholder="Write a comment..."
          />
          <button
            type="submit"
            className="self-end px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700"
          >
            Add Comment
          </button>
        </form>
      )}
    </div>
  );
}
