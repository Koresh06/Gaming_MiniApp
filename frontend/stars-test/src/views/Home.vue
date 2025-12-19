<script setup>
import { onMounted, ref } from "vue";
import { fetchGames } from "../api/games";
import { GAME_EMOJI } from "../constants/games";

const games = ref([]);
const error = ref("");

onMounted(async () => {
  try {
    games.value = await fetchGames();
  } catch (e) {
    error.value = e.message || "Failed to load games";
  }
});
</script>

<template>
  <div class="min-h-screen bg-[var(--tg-theme-bg-color)] px-4 py-6">
    <div class="max-w-md mx-auto space-y-4">

      <!-- Title -->
      <h2 class="text-xl font-semibold text-center text-[var(--tg-theme-text-color)]">
        Choose a game
      </h2>

      <!-- Error -->
      <p
        v-if="error"
        class="text-sm text-red-400 text-center"
      >
        {{ error }}
      </p>

      <!-- Games list -->
      <div class="space-y-3">
        <router-link
          v-for="game in games"
          :key="game.code"
          :to="`/game/${game.code}`"
          class="flex items-center justify-between
                 bg-[var(--tg-theme-secondary-bg-color)]
                 rounded-2xl px-4 py-3
                 shadow
                 active:scale-[0.98]
                 transition"
        >
          <div class="flex items-center gap-3">
            <span class="text-2xl">
              {{ GAME_EMOJI[game.code] || "🎮" }}
            </span>

            <span class="text-base text-[var(--tg-theme-text-color)]">
              {{ game.name }}
            </span>
          </div>

          <span class="text-[var(--tg-theme-hint-color)] text-sm">
            ▶
          </span>
        </router-link>
      </div>
    </div>
  </div>
</template>
