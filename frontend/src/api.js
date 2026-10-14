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


export function listBoards(token) {
  return request("/boards", {
    headers: { Authorization: `Bearer ${token}` },
  });
}


export function createBoard(token, name) {
  return request("/boards", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name }),
  });
}


export function joinBoard(token, invitationCode) {
  return request("/boards/join", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ invitation_code: invitationCode }),
  });
}


export function getInvitationCode(token, boardId) {
  return request(`/boards/${boardId}/invitation-code`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}


export function listParticipants(token, boardId) {
  return request(`/boards/${boardId}/participants`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}


export function createParticipant(token, boardId, name) {
  return request(`/boards/${boardId}/participants`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name }),
  });
}


export function listExpenses(token, boardId) {
  return request(`/boards/${boardId}/expenses`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}


export function createExpense(token, boardId, expense) {
  return request(`/boards/${boardId}/expenses`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(expense),
  });
}


export function getExpense(token, boardId, expenseId) {
  return request(`/boards/${boardId}/expenses/${expenseId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

