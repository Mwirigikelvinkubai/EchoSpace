import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const [form, setForm] = useState({ username: "", password: "" });
  const { login } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    // TEMP: Simulate a signup
    login({ username: form.username });
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl mb-4 font-bold">Sign Up</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Username"
          className="w-full border p-2"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full border p-2"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2">
          Sign Up
        </button>
      </form>
    </div>
  );
}
