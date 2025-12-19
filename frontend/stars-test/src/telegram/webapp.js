export function getTelegramInitData() {
  const tg = window.Telegram?.WebApp;
  if (!tg?.initData) {
    throw new Error("Telegram WebApp not available");
  }
  return tg.initData;
}
