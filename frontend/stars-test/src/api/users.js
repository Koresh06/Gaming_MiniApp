import { apiFetch } from "./http"


export function getUserByTgId(tgId) {
  return apiFetch(`/users/tg/${tgId}`);
}

export function createUser(user) {
  return apiFetch("/users/", {
    method: "POST",
    body: JSON.stringify(user),
  });
}
