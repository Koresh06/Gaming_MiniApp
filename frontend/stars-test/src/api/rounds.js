import { apiFetch } from "./http"

export function playRound(betUuid) {
  return apiFetch("/rounds/play", {
    method: "POST",
    body: JSON.stringify({
      bet_uuid: betUuid,
    }),
  });
}

export function getRound(roundUuid) {
  return apiFetch(`/rounds/${roundUuid}`);
}
