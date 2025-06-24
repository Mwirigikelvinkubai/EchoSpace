import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-indigo-600 text-white px-4 py-3 flex justify-between items-center">
      <Link to="/" className="font-bold text-xl">EchoSpace</Link>

      <div className="space-x-4">
        <Link to="/feed" className="hover:underline">Feed</Link>

        {user ? (
          <>
            <Link to="/me" className="hover:underline">Me</Link>
            <span className="text-sm">Hello, {user.username}</span>
            <button onClick={logout} className="underline">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:underline">Login</Link>
            <Link to="/signup" className="hover:underline">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
}
