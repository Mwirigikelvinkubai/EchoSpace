// src/context/AuthContext.js
import { createContext, useState, useEffect, useContext } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const fetchWithAutoRefresh = async (path, options = {}) => {
    let res = await fetch(`/api${path}`, {
      ...options,
      credentials: "include",
    });

    if (res.status === 401) {
      const refreshRes = await fetch("/api/refresh", {
        method: "POST",
        credentials: "include",
      });

      if (refreshRes.ok) {
        res = await fetch(`/api${path}`, {
          ...options,
          credentials: "include",
        });
      } else {
        setUser(null);
      }
    }

    return res;
  };

  const fetchUser = async () => {
    const res = await fetchWithAutoRefresh("/me");
    if (res.ok) {
      const data = await res.json();
      setUser(data);
      return true;
    } else {
      setUser(null);
      return false;
    }
  };

  const login = async ({ username, password }) => {
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (res.ok) {
        await fetchUser();
        return true;
      }
    } catch (err) {
      console.error("Login error:", err);
    }

    return false;
  };

  const logout = async () => {
    await fetch("/api/logout", {
      method: "POST",
      credentials: "include",
    });
    setUser(null);
  };

  const fetchMe = async () => {
    const res = await fetchWithAutoRefresh("/me");
    if (res.ok) {
      return await res.json();
    }
    return null;
  };

  useEffect(() => {
    fetchUser();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        setUser,
        fetchUser,
        fetchMe,
        fetchWithAutoRefresh,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
