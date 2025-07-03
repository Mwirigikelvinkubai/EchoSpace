export const API_BASE = "http://127.0.0.1:5000/api";

export const apiFetch = (path, options = {}) => {
  return fetch(`${API_BASE}${path}`, {
    credentials: "include",
    ...options,
  });
};
