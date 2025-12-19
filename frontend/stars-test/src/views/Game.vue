<script setup>
import { ref, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { currentUser } from "../store/user";
import { createBet, initBetPayment, getBet } from "../api/bets";
import { playRound, getRound } from "../api/rounds";
import { processPayout } from "../api/payouts";

const route = useRoute();
const router = useRouter();
const gameCode = route.params.code;

// state
const betAmount = ref(1);
const betUuid = ref(null);
const roundResult = ref(null);

const status = ref("idle");
/*
idle
creating
payment
waiting_payment
playing
finished
error
*/

const error = ref("");

// polling
let pollTimer = null;
let isPolling = false;

// navigation
function goBack() {
  router.push("/");
}

// polling utils
function stopPolling() {
  isPolling = false;
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

function startPollingPayment() {
  if (isPolling) return;

  isPolling = true;
  status.value = "waiting_payment";

  pollTimer = setInterval(async () => {
    if (!isPolling) return;

    try {
      const bet = await getBet(betUuid.value);
      const betStatus = bet.status?.toLowerCase();

      if (betStatus === "paid") {
        stopPolling();
        await startGame();
        return;
      }

      if (betStatus === "cancelled") {
        stopPolling();
        status.value = "idle";
        return;
      }
    } catch (e) {
      console.error("Polling error:", e);
    }
  }, 1500);
}

// game flow
async function startGame() {
  status.value = "playing";

  const round = await playRound(betUuid.value);
  const result = await getRound(round.uuid);
  roundResult.value = result;

  // 🔥 payout on win
  if (result.is_win === true) {
    try {
      await processPayout(result.uuid);
    } catch (e) {
      console.error("Payout error:", e);
    }
  }

  status.value = "finished";
}

// main action
async function onPlaceBet() {
  if (!currentUser.value?.uuid) {
    error.value = "User not initialized";
    return;
  }

  try {
    error.value = "";
    status.value = "creating";

    const bet = await createBet({
      user_uuid: currentUser.value.uuid,
      game_code: gameCode,
      amount: betAmount.value,
    });

    betUuid.value = bet.uuid;

    status.value = "payment";
    const { invoice_link } = await initBetPayment(bet.uuid);

    const tg = window.Telegram?.WebApp;
    if (!tg) throw new Error("Telegram WebApp not available");

    tg.openInvoice(invoice_link, (res) => {
      if (res === "paid") startPollingPayment();
      if (res === "cancelled") status.value = "idle";
    });

  } catch (e) {
    error.value = e.message || String(e);
    status.value = "error";
  }
}

onBeforeUnmount(stopPolling);
</script>

<template>
  <div class="min-h-screen bg-[var(--tg-theme-bg-color)] flex justify-center px-4 py-6">
    <div class="w-full max-w-md space-y-4">

      <!-- Back -->
      <button
        @click="goBack"
        class="text-blue-400 text-sm flex items-center gap-1"
      >
        ← Back
      </button>

      <!-- Title -->
      <h2 class="text-xl font-semibold text-center text-[var(--tg-theme-text-color)]">
        {{ gameCode.toUpperCase() }}
      </h2>

      <!-- Card -->
      <div class="bg-[var(--tg-theme-secondary-bg-color)] rounded-2xl p-4 shadow space-y-4">

        <!-- Idle -->
        <div v-if="status === 'idle'" class="space-y-3">
          <label class="text-sm text-[var(--tg-theme-hint-color)]">
            Bet amount (⭐)
          </label>

          <input
            type="number"
            v-model="betAmount"
            min="1"
            class="w-full px-3 py-2 rounded-xl bg-black/20 text-white outline-none"
          />

          <button
            @click="onPlaceBet"
            class="w-full py-2 rounded-xl font-medium
                   bg-[var(--tg-theme-button-color)]
                   text-[var(--tg-theme-button-text-color)]"
          >
            Place bet ⭐
          </button>
        </div>

        <!-- States -->
        <div v-else class="text-center space-y-2 text-white">
          <p v-if="status === 'creating'">Creating bet…</p>
          <p v-else-if="status === 'payment'">Opening payment…</p>
          <p v-else-if="status === 'waiting_payment'">Waiting for payment…</p>
          <p v-else-if="status === 'playing'" class="animate-pulse">
            🎮 Playing…
          </p>

          <!-- Result -->
          <div v-else-if="status === 'finished'" class="space-y-2">
            <h3
              v-if="roundResult?.is_win"
              class="text-2xl font-bold text-green-400"
            >
              🎉 YOU WIN!
            </h3>

            <h3
              v-else
              class="text-2xl font-bold text-red-400"
            >
              😢 You lose
            </h3>

            <p v-if="roundResult?.is_win" class="text-lg">
              +{{ roundResult.win_amount }} ⭐
            </p>

            <button
              @click="goBack"
              class="w-full mt-2 py-2 rounded-xl font-medium
                     bg-[var(--tg-theme-button-color)]
                     text-[var(--tg-theme-button-text-color)]"
            >
              Back to games
            </button>
          </div>
        </div>
      </div>

      <!-- Error -->
      <p v-if="error" class="text-red-400 text-sm text-center">
        {{ error }}
      </p>
    </div>
  </div>
</template>
