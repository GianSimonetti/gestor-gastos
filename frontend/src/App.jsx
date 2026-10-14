import { useEffect, useMemo, useState } from "react";

import {
  createBoard,
  createExpense,
  createParticipant,
  getCurrentAccount,
  getExpense,
  getInvitationCode,
  joinBoard,
  listBoards,
  listExpenses,
  listParticipants,
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
  const [selectedBoardId, setSelectedBoardId] = useState(null);
  const [participants, setParticipants] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [expenseDetail, setExpenseDetail] = useState(null);
  const [boardName, setBoardName] = useState("");
  const [participantName, setParticipantName] = useState("");
  const [expenseForm, setExpenseForm] = useState({
    name: "",
    amount: "",
    category: "",
    date: "",
    payer_id: "",
    person_id: "",
    description: "",
  });
  const [invitationCode, setInvitationCode] = useState("");
  const [sharedCode, setSharedCode] = useState("");
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState(false);
  const token = session.read();

  useEffect(() => {
    listBoards(token)
      .then((result) => {
        setBoards(result);
        setSelectedBoardId((current) => current ?? result[0]?.id ?? null);
      })
      .catch((error) => setMessage(error.message));
  }, [token]);

  useEffect(() => {
    if (selectedBoardId === null) {
      setParticipants([]);
      setExpenses([]);
      setExpenseDetail(null);
      return;
    }
    Promise.all([
      listParticipants(token, selectedBoardId),
      listExpenses(token, selectedBoardId),
    ])
      .then(([participantResult, expenseResult]) => {
        setParticipants(participantResult);
        setExpenses(expenseResult);
        setExpenseDetail(null);
        setExpenseForm((current) => {
          const ids = participantResult.map(({ id }) => String(id));
          const fallback = ids[0] ?? "";
          return {
            ...current,
            payer_id: ids.includes(current.payer_id)
              ? current.payer_id
              : fallback,
            person_id: ids.includes(current.person_id)
              ? current.person_id
              : fallback,
          };
        });
      })
      .catch((error) => setMessage(error.message));
  }, [selectedBoardId, token]);

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

  function submitParticipant(event) {
    event.preventDefault();
    run(async () => {
      await createParticipant(token, selectedBoardId, participantName);
      setParticipantName("");
      const result = await listParticipants(token, selectedBoardId);
      setParticipants(result);
      setExpenseForm((current) => ({
        ...current,
        payer_id: current.payer_id || String(result[0]?.id ?? ""),
        person_id: current.person_id || String(result[0]?.id ?? ""),
      }));
    });
  }

  function changeExpenseField(event) {
    const { name, value } = event.target;
    setExpenseForm((current) => ({ ...current, [name]: value }));
  }

  function submitExpense(event) {
    event.preventDefault();
    run(async () => {
      const payload = {
        name: expenseForm.name,
        amount: expenseForm.amount,
        category: expenseForm.category,
        payer_id: Number(expenseForm.payer_id),
        person_id: Number(expenseForm.person_id),
        description: expenseForm.description || null,
      };
      if (expenseForm.date) payload.date = expenseForm.date;
      await createExpense(token, selectedBoardId, payload);
      setExpenses(await listExpenses(token, selectedBoardId));
      setExpenseDetail(null);
      setExpenseForm((current) => ({
        ...current,
        name: "",
        amount: "",
        category: "",
        date: "",
        description: "",
      }));
    });
  }

  async function revealExpense(expenseId) {
    setMessage("");
    try {
      setExpenseDetail(
        await getExpense(token, selectedBoardId, expenseId),
      );
    } catch (error) {
      setMessage(error.message);
    }
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
            <li
              className={board.id === selectedBoardId ? "selected" : ""}
              key={board.id}
            >
              <strong>{board.name}</strong>
              <span className="row-actions">
                <button
                  className="link inline"
                  onClick={() => setSelectedBoardId(board.id)}
                  type="button"
                >
                  Abrir
                </button>
                <button
                  className="link inline"
                  onClick={() => revealCode(board.id)}
                  type="button"
                >
                  Ver código
                </button>
              </span>
            </li>
          ))}
        </ul>
        {boards.length === 0 && (
          <p className="empty">Todavía no pertenecés a ningún tablero.</p>
        )}

        {selectedBoardId !== null && (
          <>
            <section className="board-section">
              <h2>Participantes</h2>
              <form className="inline-form" onSubmit={submitParticipant}>
                <label>
                  Nombre
                  <input
                    maxLength="100"
                    onChange={(event) => setParticipantName(event.target.value)}
                    required
                    value={participantName}
                  />
                </label>
                <button disabled={pending} type="submit">
                  Agregar participante
                </button>
              </form>
              <ul className="compact-list">
                {participants.map((participant) => (
                  <li key={participant.id}>{participant.name}</li>
                ))}
              </ul>
              {participants.length === 0 && (
                <p className="empty">Todavía no hay participantes.</p>
              )}
            </section>

            <section className="board-section">
              <h2>Gastos personales</h2>
              {participants.length > 0 ? (
                <form className="expense-form" onSubmit={submitExpense}>
                  <label>
                    Nombre
                    <input
                      maxLength="100"
                      name="name"
                      onChange={changeExpenseField}
                      required
                      value={expenseForm.name}
                    />
                  </label>
                  <label>
                    Monto ARS
                    <input
                      min="0.01"
                      name="amount"
                      onChange={changeExpenseField}
                      required
                      step="0.01"
                      type="number"
                      value={expenseForm.amount}
                    />
                  </label>
                  <label>
                    Categoría
                    <input
                      maxLength="100"
                      name="category"
                      onChange={changeExpenseField}
                      required
                      value={expenseForm.category}
                    />
                  </label>
                  <label>
                    Fecha
                    <input
                      name="date"
                      onChange={changeExpenseField}
                      type="date"
                      value={expenseForm.date}
                    />
                  </label>
                  <label>
                    Pagador
                    <select
                      name="payer_id"
                      onChange={changeExpenseField}
                      required
                      value={expenseForm.payer_id}
                    >
                      {participants.map((participant) => (
                        <option key={participant.id} value={participant.id}>
                          {participant.name}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Asignado a
                    <select
                      name="person_id"
                      onChange={changeExpenseField}
                      required
                      value={expenseForm.person_id}
                    >
                      {participants.map((participant) => (
                        <option key={participant.id} value={participant.id}>
                          {participant.name}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className="full-row">
                    Descripción opcional
                    <textarea
                      maxLength="1000"
                      name="description"
                      onChange={changeExpenseField}
                      value={expenseForm.description}
                    />
                  </label>
                  <button className="full-row" disabled={pending} type="submit">
                    Registrar gasto personal
                  </button>
                </form>
              ) : (
                <p className="empty">
                  Agregá un participante para registrar gastos.
                </p>
              )}

              <ul className="expense-list">
                {expenses.map((expense) => (
                  <li key={expense.id}>
                    <span>
                      <strong>{expense.name}</strong>
                      <small>
                        {expense.category} · ARS {expense.amount} · {expense.date}
                      </small>
                    </span>
                    <button
                      className="link inline"
                      onClick={() => revealExpense(expense.id)}
                      type="button"
                    >
                      Ver detalle
                    </button>
                  </li>
                ))}
              </ul>
              {expenses.length === 0 && (
                <p className="empty">Todavía no hay gastos.</p>
              )}

              {expenseDetail && (
                <article className="expense-detail">
                  <h3>{expenseDetail.name}</h3>
                  <p>ARS {expenseDetail.amount} · {expenseDetail.category}</p>
                  <p>Fecha: {expenseDetail.date}</p>
                  <p>Tipo: personal</p>
                  <p>Pagador: participante #{expenseDetail.payer_id}</p>
                  <p>
                    Asignación: participante #{expenseDetail.allocations[0].participant_id},
                    {" "}ARS {expenseDetail.allocations[0].amount}
                  </p>
                  {expenseDetail.description && <p>{expenseDetail.description}</p>}
                </article>
              )}
            </section>
          </>
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

