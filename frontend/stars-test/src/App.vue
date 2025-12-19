<script setup>
import { onMounted, ref } from "vue";
import { initUser, currentUser } from "./store/user";

const status = ref("loading");
const error = ref("");

onMounted(async () => {
  try {
    await initUser();
    status.value = "ready";
  } catch (e) {
    status.value = "error";
    error.value = e.message;
  }
});
</script>

<template>
  <router-view />
</template>




<!-- <script setup>
import { ref, onMounted } from "vue";

const status = ref("idle");
const log = ref("");

const API_BASE_URL = `${import.meta.env.VITE_BACKEND_PROTOCOL}://${import.meta.env.VITE_BACKEND_HOST}`;

function getTelegramWebApp() {
  const tg = window.Telegram?.WebApp;
  return tg && tg.initData ? tg : null;
}

async function pay() {
  const tg = getTelegramWebApp();

  if (!tg) {
    status.value = "error";
    log.value = "Not in Telegram Mini App or context lost";
    return;
  }

  try {
    status.value = "requesting";

    const res = await fetch(
      `${API_BASE_URL}/bets/019b2e60-47cf-79b7-8c22-8e2932cd750f/init`,
      { method: "POST" }
    );

    if (!res.ok) {
      throw new Error(`Backend error: ${res.status}`);
    }

    const data = await res.json();
    const invoiceLink = data.invoice_link;

    if (!invoiceLink) {
      throw new Error("invoice_link not returned from backend");
    }

    status.value = "opening";

    tg.ready();

    tg.openInvoice(invoiceLink, (result) => {
      log.value = `Invoice result: ${result}`;
      status.value = result;
    });

  } catch (err) {
    status.value = "error";
    log.value = err.message || String(err);
  }
}


onMounted(() => {
  const tg = window.Telegram?.WebApp;

  if (tg) {
    tg.ready();
    tg.expand();
  }
});
</script>

<template>
  <div style="padding: 20px; text-align: center">
    <h2>⭐ Telegram Stars Test</h2>

    <button
      @click="pay"
      style="padding: 12px 20px; font-size: 18px"
    >
      Pay 10 ⭐
    </button>

    <p>Status: {{ status }}</p>
    <pre>{{ log }}</pre>
  </div>
</template> -->
