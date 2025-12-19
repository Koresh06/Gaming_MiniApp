import { apiFetch } from "./http"

export function processPayout(roundUuid) {
  return apiFetch(`/payouts/${roundUuid}/process`, {
    method: "POST",
  });
}
