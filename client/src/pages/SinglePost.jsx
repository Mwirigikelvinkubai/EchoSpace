import { useParams } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function SinglePost() {
  const { id } = useParams();
  const { user } = useAuth();

  // Mocked post + comment data
  const [post] = useState({
    id,
    author: "Kelvin",
    content: "Feeling hopeful today.",
    is_anonymous: false,
  });

  const [comments, setComments] = useState([
    { id: 1, author: "Jane", text: "Sending love 💖" },
    { id: 2, author: "Anonymous", text: "You're not alone." },
  ]);

  const [text, setText] = useState("");

  const handleComment = (e) => {
    e.preventDefault();
    if (!user) return alert("Login to comment.");
    const newComment = {
      id: comments.length + 1,
      author: user.username || "Anonymous",
      text,
    };
    setComments([...comments, newComment]);
    setText("");
  };

  return (
    <div className="max-w-2xl mx-auto mt-6">
      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-2">Post</h2>
        <p className="text-gray-800">{post.content}</p>
        <div className="text-sm text-gray-600 mt-2">
          — {post.is_anonymous ? "Anonymous" : post.author}
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h3 className="text-lg font-semibold mb-3">Comments</h3>
        {comments.map((c) => (
          <div key={c.id} className="border-b py-2">
            <span className="font-semibold text-sm">{c.author}:</span>{" "}
            <span>{c.text}</span>
          </div>
        ))}

        <form onSubmit={handleComment} className="mt-4 space-y-2">
          <textarea
            rows="2"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full border p-2 rounded"
            placeholder="Add a comment..."
            required
          />
          <button
            type="submit"
            className="bg-indigo-600 text-white px-4 py-1 rounded"
          >
            Post Comment
          </button>
        </form>
      </div>
    </div>
  );
}
