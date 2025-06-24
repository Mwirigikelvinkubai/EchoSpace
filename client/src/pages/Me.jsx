import { useAuth } from "../context/AuthContext";
import { useState } from "react";

export default function Me() {
  const { user } = useAuth();
  const [moods, setMoods] = useState([]);
  const [form, setForm] = useState({ mood: "", note: "" });

  if (!user) return <p className="p-4">Please log in to view your journal.</p>;

  const handleSubmit = (e) => {
    e.preventDefault();
    const entry = {
      id: moods.length + 1,
      mood: form.mood,
      note: form.note,
      date: new Date().toLocaleString(),
    };
    setMoods([entry, ...moods]);
    setForm({ mood: "", note: "" });
  };

  const handleDelete = (id) => {
    setMoods(moods.filter((m) => m.id !== id));
  };

  return (
    <div className="max-w-2xl mx-auto mt-6">
      <h1 className="text-2xl font-bold mb-4">My Mood Journal</h1>

      <form onSubmit={handleSubmit} className="bg-white p-4 rounded shadow space-y-3 mb-6">
        <input
          type="text"
          placeholder="Current mood (e.g. sad, hopeful)"
          className="w-full border p-2"
          value={form.mood}
          onChange={(e) => setForm({ ...form, mood: e.target.value })}
          required
        />
        <textarea
          rows="3"
          placeholder="Write your thoughts..."
          className="w-full border p-2"
          value={form.note}
          onChange={(e) => setForm({ ...form, note: e.target.value })}
        />
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">
          Log Mood
        </button>
      </form>

      <div className="space-y-4">
        {moods.map((entry) => (
          <div key={entry.id} className="bg-gray-100 p-4 rounded shadow-sm">
            <div className="text-sm text-gray-600">{entry.date}</div>
            <div className="font-semibold">Mood: {entry.mood}</div>
            <p>{entry.note}</p>
            <button
              onClick={() => handleDelete(entry.id)}
              className="mt-2 text-sm text-red-500 hover:underline"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
