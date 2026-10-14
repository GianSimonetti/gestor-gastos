const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";


async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail ?? "No se pudo completar la operación");
  }
  return body;
}


export function register(credentials) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}


export function login(credentials) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}


export function getCurrentAccount(token) {
  return request("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

