import { useEffect, useMemo, useState } from "react";

import { getCurrentAccount, login, register } from "./api";
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
      <main className="shell">
        <section className="card">
          <p className="eyebrow">Sesión activa</p>
          <h1>Hola, {account.email}</h1>
          <p>Tu cuenta está lista para crear un tablero.</p>
          <button className="secondary" onClick={logout} type="button">
            Cerrar sesión
          </button>
        </section>
      </main>
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

