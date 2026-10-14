import { describe, expect, it } from "vitest";

import { createSessionStore } from "./session";


function createMemoryStorage() {
  const values = new Map();
  return {
    getItem: (key) => values.get(key) ?? null,
    removeItem: (key) => values.delete(key),
    setItem: (key, value) => values.set(key, value),
  };
}


describe("session store", () => {
  it("stores the JWT and removes it on logout", () => {
    const session = createSessionStore(createMemoryStorage());

    session.save("header.payload.signature");
    expect(session.read()).toBe("header.payload.signature");

    session.clear();
    expect(session.read()).toBeNull();
  });
});
