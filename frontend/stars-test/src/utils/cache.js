export function setCache(key, data, ttlMs) {
  const record = {
    data,
    expiresAt: Date.now() + ttlMs,
  };
  localStorage.setItem(key, JSON.stringify(record));
}

export function getCache(key) {
  const raw = localStorage.getItem(key);
  if (!raw) return null;

  try {
    const record = JSON.parse(raw);
    if (Date.now() > record.expiresAt) {
      localStorage.removeItem(key);
      return null;
    }
    return record.data;
  } catch {
    localStorage.removeItem(key);
    return null;
  }
}

export function clearCache(key) {
  localStorage.removeItem(key);
}
