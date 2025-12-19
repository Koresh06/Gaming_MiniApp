import { ref } from "vue";
import { createUser, getUserByTgId } from "../api/users";

export const currentUser = ref(null);
const STORAGE_KEY = "tg_user_uuid";

export async function initUser() {
  const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
  if (!tgUser) throw new Error("Telegram user not found");

  try {
    // 🔥 ИСТИНА — backend
    const user = await getUserByTgId(tgUser.id);
    currentUser.value = user;
    localStorage.setItem(STORAGE_KEY, user.uuid);
    return user;
  } catch {
    // пользователя нет → создаём
    const payload = {
      tg_id: tgUser.id,
      username: tgUser.username || "",
      first_name: tgUser.first_name || "",
      last_name: tgUser.last_name || "",
      language_code: tgUser.language_code || "en",
    };

    const user = await createUser(payload);
    currentUser.value = user;
    localStorage.setItem(STORAGE_KEY, user.uuid);
    return user;
  }
}
