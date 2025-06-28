import { createContext, useState, useEffect, useContext } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // Load user + token from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUsername = localStorage.getItem("username");

    if (storedToken && storedUsername) {
      setToken(storedToken);
      setUser({ username: storedUsername });
    }
  }, []);

  const login = ({ username, token }) => {
    setUser({ username });
    setToken(token);
    localStorage.setItem("token", token);
    localStorage.setItem("username", username);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("username");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use the Auth context
export function useAuth() {
  return useContext(AuthContext);
}
