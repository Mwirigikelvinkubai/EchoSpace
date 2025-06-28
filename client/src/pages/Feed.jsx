import { useState } from "react";
import PostCard from "../components/PostCard";
import { useAuth } from "../context/AuthContext";

export default function Feed() {
  const { user } = useAuth();
  const [posts, setPosts] = useState([
    { id: 1, author: "Kelvin", content: "Feeling hopeful today.", is_anonymous: false },
    { id: 2, author: "Alex", content: "Some days are heavy.", is_anonymous: true },
  ]);

  const [form, setForm] = useState({ content: "", is_anonymous: false });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!user) return alert("Please log in to post.");
    const newPost = {
      id: posts.length + 1,
      author: user.username,
      content: form.content,
      is_anonymous: form.is_anonymous,
    };
    setPosts([newPost, ...posts]);
    setForm({ content: "", is_anonymous: false });
  };

  return (
    <div className="max-w-2xl mx-auto mt-6">
      <h1 className="text-2xl font-bold mb-4">EchoSpace Feed</h1>

      <form onSubmit={handleSubmit} className="mb-6 bg-white p-4 rounded shadow">
        <textarea
          value={form.content}
          onChange={(e) => setForm({ ...form, content: e.target.value })}
          className="w-full p-2 border rounded mb-2"
          placeholder="Share your thoughts..."
          rows="4"
        />
        <div className="flex justify-between items-center">
          <label className="flex items-center space-x-2 text-sm">
            <input
              type="checkbox"
              checked={form.is_anonymous}
              onChange={(e) => setForm({ ...form, is_anonymous: e.target.checked })}
            />
            <span>Post anonymously</span>
          </label>
          <button type="submit" className="bg-indigo-600 text-white px-4 py-1 rounded">
            Post
          </button>
        </div>
      </form>

      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}