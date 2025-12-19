import { apiFetch } from "./http"

export function createBet(payload) {
  return apiFetch("/bets/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function initBetPayment(betUuid) {
  return apiFetch(`/bets/${betUuid}/init`, {
    method: "POST",
  });
}

export function getBet(betUuid) {
  return apiFetch(`/bets/${betUuid}`);
}
