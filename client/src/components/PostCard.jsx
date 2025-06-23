import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const emojiSet = ["💖", "🤗", "🙏", "🌟", "💪"];

export default function PostCard({ post }) {
  const { user } = useAuth();
  const [reactions, setReactions] = useState(
    emojiSet.reduce((acc, emoji) => ({ ...acc, [emoji]: 0 }), {})
  );

  const handleReact = (emoji) => {
    if (!user) return alert("Login to react.");
    setReactions({ ...reactions, [emoji]: reactions[emoji] + 1 });
  };

  return (
    <div className="border p-4 rounded shadow mb-4 bg-white">
      <div className="text-sm text-gray-600 mb-2">
        {post.is_anonymous ? "Anonymous" : post.author}
      </div>
      <p className="text-gray-800 mb-2">{post.content}</p>

      {/* Emoji Reactions */}
      <div className="flex space-x-2 text-xl mb-2">
        {emojiSet.map((emoji) => (
          <button
            key={emoji}
            onClick={() => handleReact(emoji)}
            className="hover:scale-110 transition-transform"
            title="React"
          >
            {emoji} <span className="text-sm">({reactions[emoji]})</span>
          </button>
        ))}
      </div>

      <Link
        to={`/posts/${post.id}`}
        className="text-sm text-indigo-600 hover:underline"
      >
        View & Comment
      </Link>
    </div>
  );
}
