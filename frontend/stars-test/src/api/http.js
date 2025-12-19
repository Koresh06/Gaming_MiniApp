import { API_BASE_URL } from "../config/env";
import { getToken, clearToken } from "../auth/token";
import { telegramAuthOnce } from "./auth";

export async function apiFetch(path, options = {}, retry = true) {
  let token = getToken();

  if (!token) {
    await telegramAuthOnce();
    token = getToken();
  }

  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.status === 401 && retry) {
    clearToken();
    await telegramAuthOnce();
    return apiFetch(path, options, false);
  }

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}
