import { API_BASE_URL } from "../config/env";
import { getTelegramInitData } from "../telegram/webapp";
import { saveToken, clearToken } from "../auth/token";

let authPromise = null;

export async function telegramAuthOnce() {
  if (!authPromise) {
    authPromise = (async () => {
      const res = await fetch(`${API_BASE_URL}/auth/telegram`, {
        method: "POST",
        headers: {
          "X-Telegram-Init-Data": getTelegramInitData(),
        },
      });

      if (!res.ok) {
        clearToken();
        throw new Error("Telegram auth failed");
      }

      const data = await res.json();
      saveToken(data.access_token);
      return data;
    })().finally(() => {
      authPromise = null;
    });
  }

  return authPromise;
}
