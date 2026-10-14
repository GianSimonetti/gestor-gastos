const TOKEN_KEY = "gestor-gastos.jwt";


export function createSessionStore(storage = globalThis.localStorage) {
  return {
    clear() {
      storage.removeItem(TOKEN_KEY);
    },
    read() {
      return storage.getItem(TOKEN_KEY);
    },
    save(token) {
      storage.setItem(TOKEN_KEY, token);
    },
  };
}

