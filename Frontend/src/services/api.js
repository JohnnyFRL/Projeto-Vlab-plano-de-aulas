const BASE = "/lesson-plans";

async function request(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const message = data.error || `Erro ${res.status}`;
    throw new Error(message);
  }

  return data;
}

export const api = {
  list(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== "" && v !== null && v !== undefined) query.set(k, v);
    });
    const qs = query.toString();
    return request(`${BASE}${qs ? `?${qs}` : ""}`);
  },

  get(id) {
    return request(`${BASE}/${id}`);
  },

  create(body) {
    return request(BASE, { method: "POST", body: JSON.stringify(body) });
  },

  update(id, body) {
    return request(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(body) });
  },

  remove(id) {
    return request(`${BASE}/${id}`, { method: "DELETE" });
  },

  aiSuggestions(body) {
    return request(`${BASE}/ai-suggestions`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },
};
