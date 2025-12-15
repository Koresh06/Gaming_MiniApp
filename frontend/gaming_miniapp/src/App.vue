<template>
  <div class="app">
    <h1>🎮 Game Mini App</h1>

    <div v-if="!user" class="loader">Загрузка...</div>

    <div v-else>
      <p>👤 Пользователь: {{ user.username }}</p>
      <p>⭐ Баланс: {{ user.stars_balance }}</p>

      <button @click="createBet">Сделать ставку</button>

      <div v-if="round">
        <h3>🎲 Результат игры</h3>
        <p>Выигрыш: {{ round.win_amount }}</p>
        <p>Исход: {{ round.outcome_code }}</p>

        <button
          v-if="round.is_win"
          @click="processPayout"
        >
          Забрать выигрыш
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useTelegram } from "vue-tg";

const { WebApp } = useTelegram();

const user = ref(null);
const round = ref(null);

const API_URL = "https://your-backend.com"; // ← заменишь позже

// Получение профиля юзера из backend
async function loadUser() {
  const tg = WebApp.initDataUnsafe;

  const res = await fetch(`${API_URL}/users/by_tg_id/${tg.user.id}`);
  user.value = await res.json();
}

// Создание ставки → открытие Telegram Stars платежа
async function createBet() {
  const res = await fetch(`${API_URL}/bets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_uuid: user.value.uuid,
      game_code: "SOME_GAME",
      amount: 10
    })
  });

  const bet = await res.json();

  // Показываем кнопки оплаты внутри WebApp
  WebApp.openInvoice(bet.telegram_invoice_id, (status) => {
    console.log("Платёж:", status);

    if (status === "paid") {
      playGame(bet.uuid);
    }
  });
}

// Запуск игры после оплаты
async function playGame(betUuid) {
  const res = await fetch(`${API_URL}/rounds/play`, {
    method: "POST",
    body: JSON.stringify({ bet_uuid: betUuid }),
    headers: { "Content-Type": "application/json" },
  });

  round.value = await res.json();
}

// Запрос выплаты
async function processPayout() {
  await fetch(`${API_URL}/payouts/${round.value.uuid}/process`, {
    method: "POST"
  });

  alert("Ожидаем подтверждение Stars!");
}

onMounted(() => {
  WebApp.expand();
  loadUser();
});
</script>

<style>
.app {
  max-width: 400px;
  margin: auto;
  text-align: center;
}
button {
  margin-top: 15px;
  padding: 12px;
  width: 100%;
  font-size: 18px;
}
</style>
