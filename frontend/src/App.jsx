import { useEffect, useMemo, useState } from "react";

import {
  createBoard,
  getCurrentAccount,
  getInvitationCode,
  joinBoard,
  listBoards,
  login,
  register,
} from "./api";
import { createSessionStore } from "./auth/session";


function CredentialsForm({ mode, onSubmit, pending }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function submit(event) {
    event.preventDefault();
    onSubmit({ email, password });
  }

  return (
    <form onSubmit={submit}>
      <label>
        Email
        <input
          autoComplete="email"
          onChange={(event) => setEmail(event.target.value)}
          required
          type="email"
          value={email}
        />
      </label>
      <label>
        Contraseña
        <input
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          minLength="8"
          onChange={(event) => setPassword(event.target.value)}
          required
          type="password"
          value={password}
        />
      </label>
      <button disabled={pending} type="submit">
        {pending
          ? "Procesando…"
          : mode === "login"
            ? "Iniciar sesión"
            : "Crear cuenta"}
      </button>
    </form>
  );
}


function BoardWorkspace({ account, onLogout, session }) {
  const [boards, setBoards] = useState([]);
  const [boardName, setBoardName] = useState("");
  const [invitationCode, setInvitationCode] = useState("");
  const [sharedCode, setSharedCode] = useState("");
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState(false);
  const token = session.read();

  useEffect(() => {
    listBoards(token)
      .then(setBoards)
      .catch((error) => setMessage(error.message));
  }, [token]);

  async function run(action) {
    setMessage("");
    setPending(true);
    try {
      await action();
      setBoards(await listBoards(token));
    } catch (error) {
      setMessage(error.message);
    } finally {
      setPending(false);
    }
  }

  function submitBoard(event) {
    event.preventDefault();
    run(async () => {
      await createBoard(token, boardName);
      setBoardName("");
    });
  }

  function submitInvitation(event) {
    event.preventDefault();
    run(async () => {
      await joinBoard(token, invitationCode);
      setInvitationCode("");
    });
  }

  async function revealCode(boardId) {
    setMessage("");
    try {
      const result = await getInvitationCode(token, boardId);
      setSharedCode(result.invitation_code);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <main className="shell">
      <section className="card workspace">
        <div className="workspace-header">
          <div>
            <p className="eyebrow">Sesión activa</p>
            <h1>Tus tableros</h1>
            <p>{account.email}</p>
          </div>
          <button className="secondary" onClick={onLogout} type="button">
            Cerrar sesión
          </button>
        </div>

        <div className="board-actions">
          <form onSubmit={submitBoard}>
            <label>
              Nombre del tablero
              <input
                maxLength="100"
                onChange={(event) => setBoardName(event.target.value)}
                required
                value={boardName}
              />
            </label>
            <button disabled={pending} type="submit">
              Crear tablero
            </button>
          </form>

          <form onSubmit={submitInvitation}>
            <label>
              Código de invitación
              <input
                onChange={(event) => setInvitationCode(event.target.value)}
                required
                value={invitationCode}
              />
            </label>
            <button disabled={pending} type="submit">
              Unirme
            </button>
          </form>
        </div>

        {message && <p className="message">{message}</p>}
        {sharedCode && (
          <p className="invitation">
            Código para compartir: <strong>{sharedCode}</strong>
          </p>
        )}

        <ul className="board-list">
          {boards.map((board) => (
            <li key={board.id}>
              <strong>{board.name}</strong>
              <button
                className="link inline"
                onClick={() => revealCode(board.id)}
                type="button"
              >
                Ver código
              </button>
            </li>
          ))}
        </ul>
        {boards.length === 0 && (
          <p className="empty">Todavía no pertenecés a ningún tablero.</p>
        )}
      </section>
    </main>
  );
}


export default function App() {
  const session = useMemo(() => createSessionStore(), []);
  const [account, setAccount] = useState(null);
  const [mode, setMode] = useState("login");
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState(false);

  useEffect(() => {
    const token = session.read();
    if (!token) return;

    getCurrentAccount(token)
      .then(setAccount)
      .catch(() => session.clear());
  }, [session]);

  async function submit(credentials) {
    setMessage("");
    setPending(true);
    try {
      if (mode === "register") {
        await register(credentials);
        setMode("login");
        setMessage("Cuenta creada. Ya podés iniciar sesión.");
        return;
      }

      const { access_token: token } = await login(credentials);
      session.save(token);
      setAccount(await getCurrentAccount(token));
    } catch (error) {
      setMessage(error.message);
    } finally {
      setPending(false);
    }
  }

  function logout() {
    session.clear();
    setAccount(null);
    setMessage("");
  }

  if (account) {
    return (
      <BoardWorkspace
        account={account}
        onLogout={logout}
        session={session}
      />
    );
  }

  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">Gestor de gastos</p>
        <h1>{mode === "login" ? "Ingresá a tu cuenta" : "Creá tu cuenta"}</h1>
        <CredentialsForm mode={mode} onSubmit={submit} pending={pending} />
        {message && <p className="message">{message}</p>}
        <button
          className="link"
          onClick={() => {
            setMessage("");
            setMode(mode === "login" ? "register" : "login");
          }}
          type="button"
        >
          {mode === "login"
            ? "¿No tenés cuenta? Registrate"
            : "¿Ya tenés cuenta? Iniciá sesión"}
        </button>
      </section>
    </main>
  );
}

