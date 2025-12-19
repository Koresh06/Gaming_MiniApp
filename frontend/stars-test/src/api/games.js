import { apiFetch } from "./http"
import { getCache, setCache } from "../utils/cache";

const GAMES_CACHE_KEY = "games_list";
const GAMES_TTL = 60 * 60 * 1000; // 1 час

export async function fetchGames() {
  const cached = getCache(GAMES_CACHE_KEY);
  if (cached) return cached;

  const games = await apiFetch("/games/");
  setCache(GAMES_CACHE_KEY, games, GAMES_TTL);

  return games;
}
