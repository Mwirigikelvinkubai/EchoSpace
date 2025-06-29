import { createContext, useState, useEffect, useContext } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  // Helper function to automatically refresh token if access is expired
  const fetchWithAutoRefresh = async (path, options = {}) => {
    let res = await fetch(`/api${path}`, {
      ...options,
      credentials: 'include',
    });

    if (res.status === 401) {
      const refreshRes = await fetch('/api/refresh', {
        method: 'POST',
        credentials: 'include',
      });

      if (refreshRes.ok) {
        res = await fetch(`/api${path}`, {
          ...options,
          credentials: 'include',
        });
      } else {
        setUser(null);
      }
    }

    return res;
  };

  // Fetch current user
  const fetchUser = async () => {
    try {
      const res = await fetchWithAutoRefresh('/me');
      if (res.ok) {
        const data = await res.json();
        setUser(data);
        return true;
      }
    } catch (err) {
      console.error('Fetch user failed:', err);
    }

    setUser(null);
    return false;
  };

  // Fetch just the user object without updating context state
  const fetchMe = async () => {
    try {
      const res = await fetchWithAutoRefresh('/me');
      if (res.ok) {
        return await res.json();
      }
    } catch (err) {
      console.error('Fetch /me failed:', err);
    }
    return null;
  };

  // Run once on mount to load the user if token exists
  useEffect(() => {
    fetchUser();
  }, []);

  // Login handler
  const login = async (credentials) => {
    const res = await fetch('/api/login', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    });

    if (res.ok) {
      await fetchUser();
    }

    return res.ok;
  };

  // Logout handler
  const logout = async () => {
    await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include',
    });
    setUser(null);
  };

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

// Custom hook for consuming the AuthContext
export function useAuth() {
  return useContext(AuthContext);
}
