import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function PostForm({ onPostCreated }) {
  const { user } = useAuth();
  const [content, setContent] = useState("");
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!content.trim()) {
      setError("Need to add some content!");
      return;
    }

    setError(null);

    try {
      const res = await fetch("http://127.0.0.1:5000/api/posts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // ✅ use cookie-based JWT
        body: JSON.stringify({
          content,
          is_anonymous: isAnonymous,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        setError(err.error || "Failed to post");
      } else {
        const newPost = await res.json();
        onPostCreated(newPost);
        setContent("");
        setIsAnonymous(false);
      }
    } catch (err) {
      console.error("Post error:", err);
      setError("Server error — please try again later.");
    }
  };

  if (!user) {
    return (
      <p className="text-center text-gray-500 mt-4">Login to post.</p>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-4 rounded-lg shadow mb-6"
    >
      <textarea
        rows={4}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Share something..."
        className="w-full border rounded p-2 resize-none focus:ring-2 focus:ring-blue-500"
      />
      <div className="flex items-center justify-between mt-2">
        <label className="flex items-center space-x-2 text-sm">
          <input
            type="checkbox"
            checked={isAnonymous}
            onChange={(e) => setIsAnonymous(e.target.checked)}
          />
          Post anonymously
        </label>
        {error && (
          <span className="text-red-600 text-sm">{error}</span>
        )}
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700 transition"
        >
          Post
        </button>
      </div>
    </form>
  );
}
