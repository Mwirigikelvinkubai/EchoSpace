import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import CommentSection from "../components/CommentSection";

export default function PostDetail() {
  const { id } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/posts/${id}`)
      .then((res) => res.json())
      .then(setPost);
  }, [id]);

  if (!post) return <p>Loading post...</p>;

  return (
    <div className="max-w-xl mx-auto p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-2">
        {post.is_anonymous ? "Anonymous" : post.author}
      </h2>
      <p className="text-gray-700 mb-4">{post.content}</p>

      {/* ✅ Embed CommentSection here */}
      <CommentSection postId={post.id} />
    </div>
  );
}
